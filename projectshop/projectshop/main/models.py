from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from projectshop.main.managers import AppUsersManager
from projectshop.main.validators import only_letters_validator, only_numbers


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    objects = AppUsersManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    FIRST_NAME_MAX_LEN = 25
    FIRST_NAME_MIN_LEN = 2

    LAST_NAME_MAX_LEN = 25
    LAST_NAME_MIN_LEN = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            only_letters_validator
        ],
        )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=[
            MinLengthValidator(LAST_NAME_MIN_LEN),
            only_letters_validator
        ],
    )

    image = models.URLField(
        default='https://www.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.first_name


class Products(models.Model):
    NAME_MAX_LEN = 100

    name = models.CharField(
        max_length=NAME_MAX_LEN
    )

    price = models.FloatField(
        validators=[
            MinValueValidator(0.01)
        ]
    )

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )

    description = models.TextField()

    image = models.URLField()

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def total_price(self):
        cart_products = ShoppingCartProducts.objects.filter(cart=self)
        total_price = 0
        for product in cart_products:
            total_price += product.product.price * product.quantity
        return total_price


class ShoppingCartProducts(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def product_total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    NAME_MAX_LEN = 25
    NAME_MIN_LEN = 2

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=[MinLengthValidator(NAME_MIN_LEN),
                    only_letters_validator]
    )

    email = models.EmailField()
    address = models.CharField(
        max_length=100
    )
    phone = models.CharField(
        max_length=10,
        validators=[only_numbers],
    )
    city = models.CharField(
        max_length=20
    )
    state = models.CharField(
        max_length=30
    )
    zipcode = models.IntegerField()
    country = models.CharField(
        max_length=30
    )
    cart = models.ForeignKey(ShoppingCart, on_delete=models.SET_NULL, null=True)

    total_price = models.FloatField(default=0)
