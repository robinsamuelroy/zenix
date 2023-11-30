from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, ProductImages
from django.db.models import Count
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
  # products = Product.objects.all().order_by('id')
  blocked_categories =Category.objects.filter(is_blocked =True)
  products = Product.objects.filter(product_status='draft',featured=True)
  latest = Product.objects.filter(status=True).order_by("-id")[:10]
  categories =Category.objects.filter(is_blocked =False)
  user=request.user
  context = {
        "products":products,
        "latest":latest,
        "categories":categories,
        'user'  : user
  }
  return render(request, 'shop/index.html',context)

#################################################################
#listing products on the shop page:  

def product_list_view(request):
   # products = Product.objects.all().order_by('id')
  blocked_categories =Category.objects.filter(is_blocked =True)
  products = Product.objects.filter(product_status='draft')
  categories =Category.objects.filter(is_blocked =False)
  p=Paginator(Product.objects.filter(status =True).exclude(category__in=blocked_categories),10)
  page=request.GET.get('page')
  productss=p.get_page(page)

  context = {
        "products":products,
        "categories":categories,
        "productss":productss
  }
    
  return render(request,'shop/product_list.html', context)
#########################################################################

def category_list_view(request):
   # products = Product.objects.all().order_by('id')
  # categories = Category.objects.all().annotate(product_count=Count('product'))
  category = Category.objects.filter(is_blocked=False)


  context = {
    'category' : category
  }

  return render(request, 'shop/category-list.html',context)

###############################################################

def category_product_list_view(request, cid):
  category = Category.objects.get(cid=cid)
  products = Product.objects.filter(status=True,category=category)

  context = {
    'category' : category,
    'products' : products,
  }
  return render(request,'shop/category-product-list.html',context)

########################################################################################fgnhrhhh

def product_detail(request,pid):
    product = Product.objects.get(pid = pid)
    p_image =product.p_images.all()
    category = Category.objects.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    
    
    context={
        "product":product,
        "p_image":p_image,
        "category":category,
        "products":products
        
        
        
    }
    return render (request,'shop/product_detail.html',context)

def search_view(request):
    query =request.GET.get('q')
    print(query)
    
    products =Product.objects.filter(title__icontains =query)
    print(products)
    
    context ={
        'products':products,
        'query': query
        
    }
    
    return render(request,'shop/search.html',context)


# def filter_product(request):
#     categories =request.GET.getlist('Category[]')
    
#     products =Product.objects.filter(status=True).order_by('-id').distinct()
    
#     if len(categories) > 0:
#         products=products.filter(category__id__in=categories).distinct()
        
#     data =render_to_string('app1/async/product-list.html',{"products":products})
#     return JsonResponse ({"data":data})
    
def filter_product(request):    
    try:
            categories = request.GET.getlist('category[]')
            print("Selected Categories:", categories)

            products = Product.objects.filter(status=True).order_by('-id').distinct()
            print("All Products:", products)
            print("Selected Categories:", categories)

            if len(categories) > 0:
                products = products.filter(category__cid__in=categories).distinct()
                print("Filtered Product:", products)

            data = render_to_string('shop/async/product-list.html', {"products": products})
            return JsonResponse({"data": data})
    except Exception as e:
            return JsonResponse({"error": str(e)})





def product_detail_view(request,pid):
   product = Product.objects.get(pid=pid)
  #  product = get_object_or_404(product,pid=pid)

   p_image = product.p_images.all()

   context = {
     'p' : product,
     'p_image' : p_image,
   }
   return render(request, 'shop/product-detail.html',context)
  
