from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.contrib import admin

from projectshop.main.models import Profile, AppUser, Order, Products, ShoppingCart, ShoppingCartProducts


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user_id']
    search_fields = ('first_name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'country', 'total_price']
    search_fields = ('email',)
    ordering = ('email', 'total_price', 'name')
    filter_horizontal = ()


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'id']
    search_fields = ('name', 'price')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(ShoppingCartProducts)
class ShoppingCartProductsAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart']


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AppUser
        fields = ('email', 'password', 'is_staff', 'is_superuser')


class AppUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Group Permissions', {
            'fields': ('groups', 'user_permissions',)
        })
    )

    add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(AppUser, AppUserAdmin)
