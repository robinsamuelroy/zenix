
from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.html import mark_safe
from unicodedata import decimal
from accounts.models import Account
# Create your models here.

STATUS_CHOICE = (
   ('process', 'Processing'),
   ('shipped', 'Shipped'),
   ('delivered', 'Delivered'),
)

STATUS = (
   ('draft', 'Draft'),
   ('disabled', 'Disabled'),
   ('rejected', 'Rejected'),
   ('in_review', 'In_Review'),
   # ('published', 'Published'),
)

RATING = (
   (1, '⭐☆☆☆☆'),
   (2, '⭐⭐☆☆☆'),
   (3, '⭐⭐⭐☆☆'),
   (4, '⭐⭐⭐⭐☆'),
   (5, '⭐⭐⭐⭐⭐'),
)

class Category(models.Model):
   cid = ShortUUIDField(unique=True, max_length=30)

   title = models.CharField(max_length=100, default='Watches')
   image = models.ImageField(upload_to='category', default='category.jpg')
   is_blocked =models.BooleanField(default=False)

   class Meta:
      verbose_name_plural = 'Categories'
   
   def category_image(self):
      return mark_safe("<img src='%s' width ='50' height='50' />" % (self.image.url))
   
   def __str__(self):
      return self.title
   
##################################################################

#######################################################################################

class Product(models.Model):
   pid = ShortUUIDField(unique=True, max_length=30)

   user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name = 'category')

   title = models.CharField(max_length=100, default='Branded watch')
   image = models.ImageField(upload_to='product', default ='product.jpg')
   description = models.TextField(null=True, blank=True, default='This is the product')

   price = models.DecimalField(max_digits=10, decimal_places=2, default='1200.00')
   old_price = models.DecimalField(max_digits=10, decimal_places=2, default='1000.00')

   specifications = models.TextField(null=True, blank=True)


##################
   stock_count = models.CharField(max_length = 100,default = "10",null=True, blank=True)
   manufacturing_date=models.DateTimeField(auto_now_add=False,null=True, blank=True)
   return_policy= models.CharField(max_length = 100,default = "10", null=True, blank=True)
   warrenty = models.CharField(max_length = 100,default = "1", null=True, blank=True)
####################

   product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

   status = models.BooleanField(default=True)
   in_stock = models.BooleanField(default=True)
   featured = models.BooleanField(default=False)
   digital = models.BooleanField(default=False)

   sku = ShortUUIDField(unique=True, max_length=10)

   date = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(null=True, blank=True)

   

   class Meta:
       verbose_name_plural = 'Products'

   def product_image(self):
       return mark_safe("<img src='%s' width ='50' height='50' />" % (self.image.url))
   
   def __str__(self):
       return self.title
   
   def get_percentage(self):
       new_price = (self.price / self.old_price) * 100
       return new_price
   
class ProductImages(models.Model):
    images = models.ImageField(upload_to='product_images',default='product.jpg')
    product = models.ForeignKey(Product,related_name='p_images', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe("<img src='%s' width ='50' height='50' />" % (self.images.url))

    def __str__(self):
        return str(self.product) 
        





     


  