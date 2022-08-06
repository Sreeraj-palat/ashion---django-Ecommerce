from django.shortcuts import render
from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator


def home(request):
    
    products = Product.objects.filter(is_available = True)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)

    context = {
        'product':pageed_products
    } 
    return render(request, 'home.html', context)