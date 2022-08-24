from django.shortcuts import render, redirect
from orders.models import OrderProduct, Payment, Order
from accounts.models import Account
from .forms import updateuserform
# Create your views here.

def dashboard(request):
    order_product = OrderProduct.objects.filter(user=request.user)
    order = Order.objects.filter(user = request.user)
    payment = Payment.objects.filter(user = request.user)
    user = Account.objects.get(id=request.user.id)
    form=updateuserform(instance=user)
    if not request.user.is_superadmin:
            
        if request.method == 'POST':
            form=updateuserform(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')

    context = {
        'order':order,
        'order_product': order_product,
        'payment':payment,
        'form':form,
    }
    return render(request,'user_dashboard.html',context)
        


