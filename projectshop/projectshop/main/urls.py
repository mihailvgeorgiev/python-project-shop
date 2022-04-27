from django.urls import path
from . import views
from projectshop.main.views import RegisterView, UserLoginView, UserLogoutView, ProductsView

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('add_product/<int:pk>/', views.add_product, name='add_product'),
    path('remove_product/<int:pk>/', views.remove_product, name='remove_product'),
    path('', views.about_us, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('decrease_product/<int:pk>/', views.reduce_product, name='decrease_product'),
    path('increase_product/<int:pk>/', views.increase_product, name='increase_product'),
    path('details_product/<int:pk>/', views.details_product, name='details_product'),
    path('profile/', views.view_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('shopping_cart/', views.shopping_cart, name='cart'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
]