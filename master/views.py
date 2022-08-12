from django.shortcuts import render, redirect
from accounts.models import Account
from store.models import Product
from django.contrib import messages
from .forms import productForm

# Create your views here.

def dashboard(request):
    return render(request, 'master/dashboard.html')


def users(request):
    user = Account.objects.all()
    context = {
        'user' : user,
    }
    return render(request, 'master/user_list.html', context)    


def blockUser(request, id):
    user = Account.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, 'user is Blocked Successfully')
    else:
        user.is_active = True
        messages.success(request, 'user is  Unblocked Successfully')

    user.save()
    return redirect('users')      


def products(request):
    product = Product.objects.all()
    context = {
        'product' : product
    }
    return render(request, 'master/product_list.html', context)    


def AddProduct(request):
    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            messages.warning(request, 'enter the correct details')

    context = {
        'form' : form,
        }        
    return render(request, 'master/add_product.html', context)    



def EditProduct(request,id):
    product = Product.objects.get(id=id)
    form = productForm(instance=product)
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {
        'form' : form,
        'product' : product,
    }        
    return render(request, 'master/edit_product.html', context)


def DeleteProduct(request,id):
    product = Product.objects.filter(id=id)
    product.delete()
    return redirect('product_list')

    