from django.urls import path
from . import views

urlpatterns = [
    path('',views.apply_coupon,name='apply_coupon'),
    
    
]