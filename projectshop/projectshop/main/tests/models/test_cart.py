from django.core.exceptions import ValidationError
from django.test import TestCase

from projectshop.main.models import AppUser, Profile, ShoppingCart, Products, ShoppingCartProducts


class CartTests(TestCase):

    VALID_USER_DATA = {
        'email': 'aqwer@abv.bg',
        'password': 'helloWorld242',
        'id': 1
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Tested',
        'user_id': 1,
        'gender': 'Male',
    }

    VALID_PRODUCT_DATA = {
        'name': 'TestProduct1',
        'price': 10.50,
        'quantity': 5,
        'description': 'A product for test purposes',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png',
    }

    VALID_PRODUCT_DATA_2 = {
        'name': 'TestProduct2',
        'price': 40,
        'quantity': 3,
        'description': 'Another product for test purposes',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png',
    }

    def test_shopping_cart_total_price__expect_right_price(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

        cart = ShoppingCart(user=profile)
        cart.save()

        product_1 = Products(**self.VALID_PRODUCT_DATA)
        product_1.save()

        product_2 = Products(**self.VALID_PRODUCT_DATA_2)
        product_2.save()

        cart_product_1 = ShoppingCartProducts(cart=cart, product=product_1, quantity=2)
        cart_product_1.save()

        cart_product_2 = ShoppingCartProducts(cart=cart, product=product_2, quantity=3)
        cart_product_2.save()

        products = ShoppingCartProducts.objects.filter(cart=cart)
        total_price = 0
        for product in products:
            total_price += product.product.price * product.quantity

        self.assertEqual(cart.total_price, total_price)
        self.assertEqual(cart.total_price, 141)


