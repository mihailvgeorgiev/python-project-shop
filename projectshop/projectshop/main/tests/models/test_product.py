from django.core.exceptions import ValidationError
from django.test import TestCase

from projectshop.main.models import Products


class ProductTests(TestCase):

    VALID_PRODUCT_DATA = {
            'name': 'TestProduct1',
            'price': 10.50,
            'quantity': 5,
            'description': 'A product for test purposes',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png',

        }

    def test_product__call_str__expect_product_name(self):
        product = Products(**self.VALID_PRODUCT_DATA)

        self.assertEqual(str(product), product.name)