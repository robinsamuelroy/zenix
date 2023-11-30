from django.contrib import admin
from django.conf import settings  
from shop.models import Category, Product, ProductImages

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages

class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin]
  list_display = ['user', 'title', 'product_image', 'price','category', 'featured', 'product_status','pid']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title', 'category_image','cid']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin) 
