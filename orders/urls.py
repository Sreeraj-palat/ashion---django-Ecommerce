from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payment/status/',views.payment_status, name='payment_status'),
    
]