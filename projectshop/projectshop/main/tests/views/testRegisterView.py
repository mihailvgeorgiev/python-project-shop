from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):

    def test_get__expect_correct_template(self):
          response = self.client.get(reverse('register'))
          self.assertTemplateUsed(response, 'register.html')