from django.contrib import admin
from .models import Payment, Order, OrderProduct, Delivery_address

# Register your models here.


admin.site.register(Payment),
admin.site.register(Order),
admin.site.register(OrderProduct),
admin.site.register(Delivery_address),
