from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product, ReviewRating
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from .forms import ReviewForm
from django.contrib import messages






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
        paginator = Paginator(products, 9)
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
        print(keyword)    

        context = {
            'products' : products,
            'keyword' :keyword,
        }    
    return render(request, 'store.html', context)





def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)