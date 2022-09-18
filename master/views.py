import imp
from unicodedata import category
from django.shortcuts import render, redirect
from accounts.models import Account
from coupons.models import Coupons
from store.models import Product, Variation
from django.contrib import messages
from .forms import productForm, CategoryForm, VariationForm, AddCouponForm
from category.models import Category
from orders.models import Order,OrderProduct,Payment
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
# Create your views here.

def dashboard(request):

    # Total Revenue
    total_revenue = 0
    products = OrderProduct.objects.filter(ordered=True)
    for item in products :
        total_revenue += item.product_price * item.quantity


    # Total Orders
    order_total = Order.objects.filter(is_ordered=True)
    total_order_count = order_total.count()

    #user chart
    verified_user = Account.objects.filter(is_active=True, is_superadmin=False)
    not_verified_user = Account.objects.filter(is_active=False, is_superadmin=False)
    total_user = int(verified_user.count()+not_verified_user.count())
    data1=[verified_user.count(),not_verified_user.count()]
    data1_label =['Verified','Not Verified']


    # Category Chart
    order_products = OrderProduct.objects.all()
    women, men, kids, cosmetics, accessories = 0, 0, 0, 0, 0
    for order_product in order_products :
        if order_product.product.category.category_name == 'Womens Fashion' :
            women += order_product.quantity
        elif order_product.product.category.category_name == 'Mens Fashion' :
            men += order_product.quantity
        elif order_product.product.category.category_name == 'Kids Fashion' :
            kids += order_product.quantity
        elif order_product.product.category.category_name == 'Cosmetics' :
            cosmetics += order_product.quantity
        elif order_product.product.category.category_name == 'Accessories' :
            accessories += order_product.quantity    
    total_products = women + men + kids + cosmetics + accessories
    data4=[women, men, kids, cosmetics, accessories]
    print(women, men, kids, cosmetics, accessories)
    data4_label =['Womens Fashion','Mens Fashion', 'Kids Fashion', 'Cosmetics', 'Accessories']

    context = {
            
            'total_user':total_user,
            'data1':data1,
            'data1_label':data1_label,
            'data4' : data4,
            'data4_label':data4_label,
            'total_products' : total_products,
            'total_revenue' : total_revenue,
            'total_order_count' : total_order_count,
        }


    return render(request, 'master/dashboard.html', context)





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
    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)
    context = {
        'product' : pageed_products
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



def CategoryList(request):
    category = Category.objects.all()
    context = {
        'category' : category,
    }

    return render(request, 'master/category_list.html', context)



def AddCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            messages.warning(request, 'enter correct details')

    context = {
        'form' : form,
    }               

    return render(request,'master/add_category.html', context)





def EditCategory(request,id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method=='POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')

    context = {
        'form' : form,
        'category' : category,
    }        
    return render(request, 'master/edit_category.html', context)




def DeleteCategory(request,id):
    category = Category.objects.filter(id=id)
    category.delete()
    return redirect('category_list')





def VariationList(request):
    variation = Variation.objects.all()
    paginator = Paginator(variation, 5)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)
    context = {
        'variation' : pageed_products,
    }

    return render(request,'master/variation_list.html', context)




def AddVariation(request):
    form = VariationForm()
    if request.method == 'POST':
        form = VariationForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('variation_list')
        else:
            messages.warning(request, 'enter correct details')

    context = {
        'form' : form,
    }               

    return render(request,'master/add_variation.html', context)  


def EditVariation(request,id):
    variation = Variation.objects.get(id=id)
    form = VariationForm(instance=variation)
    if request.method=='POST':
        form = VariationForm(request.POST, request.FILES, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_list')

    context = {
        'form' : form,
        'variation' : variation,
    }        
    return render(request, 'master/edit_variation.html', context)      
    


def DeleteVariation(request,id):
    variation = Variation.objects.filter(id=id)
    variation.delete()
    return redirect('variation_list')    


def orders(request):
    order = Order.objects.all()
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)
    context = {
        'order' : pageed_products
    }
    return render(request,'master/orders.html', context)




def orderdetails(request, id):
    order = Order.objects.get(order_number=id)
    orderproduct = OrderProduct.objects.filter(order__order_number=id).order_by('-created_at')
    context = {
        'order' : order,
        'orderproduct':orderproduct,
    }
    return render(request,'master/order_details.html',context)




def update_order_status(request, pk):
    url = request.META.get('HTTP_REFERER')
    order_item = Order.objects.get(id=pk)
        
    if  order_item.status == 'Ordered':
        order_item.status = 'shipped'
    elif order_item.status == 'shipped':
        order_item.status = 'out_for_delivery'
    elif order_item.status == 'out_for_delivery':
        order_item.status = 'delivered'
        # if order_item.status == 'delivered':
        #     if order_item.is_paid == False:
        #         order_item.is_paid = True
        #         order_item.save()
        
    order_item.save()
    return redirect(url)




def cancel_order(request,id):
    url = request.META.get('HTTP_REFERER')
    order = Order.objects.get(order_number=id)
    if order.status != 'delivered':
        print(order.status)
        print(id)
        order.status = 'Cancelled'
        order.save()
    return redirect(url)





def coupon_list(request):
    coupons = Coupons.objects.all()
    context = {
        'coupons':coupons
    }
    return render (request,'master/coupon_list.html', context)




def add_coupon(request):
    form = AddCouponForm()
    if request.method == 'POST':
        form = AddCouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('coupon_list')
        else:
            messages.warning(request, 'enter correct details')

    context = {
        'form' : form,
    }               
    return render(request, 'master/add_coupon.html', context)    



def edit_coupon(request,id):
    coupon = Coupons.objects.get(id=id)
    form = AddCouponForm(instance = coupon)
    if request.method == 'POST':
        form = AddCouponForm(request.POST, request.FILES, instance = coupon)
        if form.is_valid():
            form.save()
        return redirect('coupon_list')
    context = {
        'form' : form,
        'coupon' : coupon,
    }        
    return render(request, 'master/edit_coupon.html', context)



def delete_coupon(request,id):
    coupon = Coupons.objects.filter(id=id)
    coupon.delete()
    return redirect('coupon_list')    
    
    



    