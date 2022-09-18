from django.shortcuts import render, redirect
from .models import Coupons
from .forms import ApplyCouponForm
from django.contrib import messages


# Create your views here.

def apply_coupon(request):
    if request.method == 'POST':
        form = ApplyCouponForm(request.POST)
        if form.is_valid():
            code = request.POST['code']
            if Coupons.objects.filter(code=code).exists():

                request.session['code'] = code
                print(code)
                messages.success(request, "Address is saved")
            return redirect('cart')

        else:
            messages.info(request, "Coupon is invalid")
            return redirect('cart')    
