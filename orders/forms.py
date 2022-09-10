from django import forms
from .models import Order, Delivery_address


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']


class addressform(forms.Form):
    class meta:
        model = Delivery_address
        fields = ['firstname','lastname','addressfield_1','addressfield_2','city','state','country','post_code','phonenumber','email']
