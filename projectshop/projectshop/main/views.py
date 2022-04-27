from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import forms as auth_forms, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from projectshop.main.forms import ProfileForm, CheckoutForm, CreateProductForm
from projectshop.main.models import Profile, Products, ShoppingCart, ShoppingCartProducts, Order
from projectshop.main.validators import only_letters_validator

UserModel = get_user_model()


def group_required(*group_names):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated or not bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return HttpResponse('No permission')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


class ProductsView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'products.html'
    model = Products
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_list'] = Products.objects.all()
        return context


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=25, validators=[only_letters_validator])
    last_name = forms.CharField(max_length=25, validators=[only_letters_validator])
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = UserModel
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
            gender=self.cleaned_data['gender'],
        )
        if commit:
            profile.save()
        return user


class RegisterView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next
        return reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):
    success_url = reverse_lazy('index')


@login_required
def view_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile,
    }

    return render(request, 'details_profile.html', context)


def add_product(request, pk):
    product = Products.objects.get(id=pk)

    user = request.user
    profile = Profile.objects.get(user=user)
    cart = ShoppingCart.objects.filter(user=profile)

    if len(cart) == 0:
        cart = ShoppingCart.objects.create(user=profile)
        cart.save()

    cart = ShoppingCart.objects.filter(user=profile).last()

    is_in = ShoppingCartProducts.objects.filter(cart=cart, product=product)
    if len(is_in) == 0:
        form = ShoppingCartProducts.objects.create(cart=cart, product=product)
        form.save()
    else:
        if is_in[0].quantity < is_in[0].product.quantity:
            is_in[0].quantity += 1
            is_in[0].save()

    return redirect(request.META['HTTP_REFERER'])


def remove_product(request, pk):

    record = ShoppingCartProducts.objects.get(id=pk)
    record.delete()

    return redirect('cart')


def reduce_product(request, pk):

    product = ShoppingCartProducts.objects.get(id=pk)
    product.quantity -= 1
    product.save()

    if product.quantity == 0:
        remove_product(request, pk)

    return redirect('cart')


def increase_product(request, pk):

    product = ShoppingCartProducts.objects.get(id=pk)

    if product.quantity < product.product.quantity:
        product.quantity += 1
        product.save()

    return redirect('cart')


@login_required
def shopping_cart(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = ShoppingCart.objects.filter(user=profile).last()
    cart_items = ShoppingCartProducts.objects.filter(cart=cart).order_by('product__name')

    total_products = 0
    total_price = 0

    for product in cart_items:
        total_products += product.quantity
        total_price += product.product.price * product.quantity

    context = {
        'products': cart_items,
        'total_products': total_products,
        'total_price': total_price,
    }

    return render(request, 'shopping_cart.html', context)


def about_us(request):

    return render(request, 'about_us.html')


@login_required
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        'form': form
    }

    return render(request, 'edit_profile.html', context)


@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    return redirect('index')


@login_required
def checkout(request):
    form = CheckoutForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = ShoppingCart.objects.filter(user=profile).last()
    products = ShoppingCartProducts.objects.filter(cart=cart)

    total_products = 0
    total_price = 0

    for product in products:
        total_products += product.quantity
        total_price += product.product.price * product.quantity

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            buy = form.save(commit=False)
            buy.cart = cart
            buy.user = profile
            buy.total_price = cart.total_price
            buy.save()

            bought_products = ShoppingCartProducts.objects.filter(cart=cart)

            for bought_product in bought_products:
                product = Products.objects.get(id=bought_product.product.id)
                product.quantity -= bought_product.quantity
                product.save()

            create_cart = ShoppingCart.objects.create(user=profile)
            create_cart.save()
            return redirect('products')

    context = {
        'form': form,
        'products': products,
        'total_products': total_products,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)


@group_required('product_team')
def create_product(request):
    form = CreateProductForm()

    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form
    }

    return render(request, 'create_product.html', context)


@group_required('product_team')
def update_product(request, pk):
    product = Products.objects.get(id=pk)
    form = CreateProductForm(instance=product)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'product_id': product.id
    }

    return render(request, 'edit_product.html', context)


@group_required('product_team')
def delete_product(request, pk):
    product = Products.objects.get(id=pk)
    product.delete()

    return redirect('products')


def details_product(request, pk):
    product = Products.objects.get(id=pk)

    context = {
        'product': product
    }

    return render(request, 'details_product.html', context)


@login_required
def order_history(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=profile)

    context = {
        'orders': orders
    }

    return render(request, 'order_history.html', context)