from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator




def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        pageed_products = paginator.get_page(page)

    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        pageed_products = paginator.get_page(page)


        
    context ={
        'product' : pageed_products,
    }
    return render(request, 'store.html', context)




def product_detail(request, category_slug, product_slug):
    try :
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
       
    except Exception as e:
        raise e 

    context = {
        'single_product' : single_product,
        'in_cart': in_cart,
    }       
    return render(request, 'product_detail.html', context)    



def search(request):
    keyword = ''
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        products = Product.objects.filter(
                Q(description__icontains=keyword) |
                Q(product_name__icontains=keyword)
            )

        context = {
            'products' : products,
            'keyword' :keyword,
        }    
    return render(request, 'store.html', context)
