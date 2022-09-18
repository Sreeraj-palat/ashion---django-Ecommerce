from dataclasses import fields
import imp
from django import forms 
from .models import Coupons



class ApplyCouponForm(forms.Form):
    class meta:
        model = Coupons
        fields = ['code']