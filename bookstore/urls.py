from django.urls import path
from . import views

app_name = 'bookstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('viewbook', views.viewBook, name='viewBook'),
    path('addtocart', views.addToCart, name='addToCart'),
    path('cart', views.viewCart, name='cart'),
]