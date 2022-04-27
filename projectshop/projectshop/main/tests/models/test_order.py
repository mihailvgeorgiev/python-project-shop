from django.core.exceptions import ValidationError
from django.test import TestCase

from projectshop.main.models import AppUser, ShoppingCart, Order, Profile


class OrderTests(TestCase):

    VALID_ORDER_DATA = {
        'name': 'Georgi',
        'email': 'avcd@gmail.com',
        'address': 'RandomAddress',
        'phone': '0993423534',
        'city': 'RandomCity',
        'state': 'RandomState',
        'zipcode': '4255',
        'country': 'TestCountry',
        'total_price': 0,
    }

    INVALID_ORDER_DATA_NAME = {
        'name': 'Georgi test',
        'email': 'avcd@gmail.com',
        'address': 'RandomAddress',
        'phone': '0993423534',
        'city': 'RandomCity',
        'state': 'RandomState',
        'zipcode': '4255',
        'country': 'TestCountry',
        'total_price': 0,
    }

    INVALID_ORDER_DATA_PHONE = {
        'name': 'Georgi',
        'email': 'avcd@gmail.com',
        'address': 'RandomAddress',
        'phone': '09934f3534',
        'city': 'RandomCity',
        'state': 'RandomState',
        'zipcode': '4255',
        'country': 'TestCountry',
        'total_price': 0,
    }

    VALID_USER_DATA = {
        'email': 'aqwer@abv.bg',
        'password': 'helloWorld242',
        'id': 1
    }

    VALID_CART_DATA = {
        'user': 1
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Tested',
        'user_id': 1,
        'gender': 'Male',
    }

    def test_order_create__when_name_contains_only_letters__expect_success(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

        cart = ShoppingCart(user=profile)
        cart.save()

        order = Order(user=profile, cart=cart, **self.VALID_ORDER_DATA)
        order.save()

    def test_order_create__when_name_contains_space__expect_fail(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

        cart = ShoppingCart(user=profile)
        cart.save()

        order = Order(**self.INVALID_ORDER_DATA_NAME)

        with self.assertRaises(ValidationError) as context:
            order.full_clean()
            order.save()

        self.assertIsNotNone(context.exception)

    def test_order_create__when_phone_contains_character__expect_fail(self):
        user = AppUser(**self.VALID_USER_DATA)
        user.save()

        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.save()

        cart = ShoppingCart(user=profile)
        cart.save()

        order = Order(**self.INVALID_ORDER_DATA_PHONE)

        with self.assertRaises(ValidationError) as context:
            order.full_clean()
            order.save()

        self.assertIsNotNone(context.exception)
