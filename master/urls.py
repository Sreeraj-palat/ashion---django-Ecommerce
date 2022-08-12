from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('user_list/',views.users, name='users'),
    path('block-user/<int:id>/',views.blockUser,name='block-user'),

    path('product_list/',views.products, name='product_list'),
    path('add_product/',views.AddProduct, name='add_product'),
    path('edit_product/<int:id>/',views.EditProduct, name='edit_product'), 
    path('delete_product/<int:id>/',views.DeleteProduct, name='delete_product'), 
   
]