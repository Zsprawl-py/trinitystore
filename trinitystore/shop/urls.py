from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('shop/', views.product_list1, name='product_list1'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_slug'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]