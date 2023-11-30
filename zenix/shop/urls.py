from django.contrib import admin
from django.urls import include, path
from .import views
from shop.views import index


app_name='shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list_view, name='product-list'),

    path('product/<pid>/', views.product_detail_view, name='product-detail'),

    path('category-list/', views.category_list_view, name='category-list'),
    path('category/<cid>/', views.category_product_list_view, name='category-product-list'),

    path('search/',views.search_view,name='search'),
    path('filter-products/', views.filter_product,name='filter-product')
]