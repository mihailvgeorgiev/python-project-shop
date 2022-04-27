from django import forms
from .models import Profile, Order, Products


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'gender',
            'image',
        ]


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name',
                  'email',
                  'address',
                  'phone',
                  'city',
                  'state',
                  'zipcode',
                  'country',
                  ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Name',
                    'class': 'form-control',
                }
            ),

            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'form-control',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Address',
                    'class': 'form-control',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Phone',
                    'class': 'form-control',
                }
            ),

            'city': forms.TextInput(
                attrs={
                    'placeholder': 'City',
                    'class': 'form-control',
                }
            ),

            'state': forms.TextInput(
                attrs={
                    'placeholder': 'State',
                    'class': 'form-control',
                }
            ),

            'zipcode': forms.NumberInput(
                attrs={
                    'placeholder': 'Zipcode',
                    'class': 'form-control',
                }
            ),

            'country': forms.TextInput(
                attrs={
                    'placeholder': 'Country',
                    'class': 'form-control',
                }
            ),
        }


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['name',
                  'quantity',
                  'price',
                  'description',
                  'image',
                  ]
