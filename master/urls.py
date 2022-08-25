from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name='admindashboard'),
    path('user_list/',views.users, name='users'),
    path('block-user/<int:id>/',views.blockUser,name='block-user'),

    path('product_list/',views.products, name='product_list'),
    path('add_product/',views.AddProduct, name='add_product'),
    path('edit_product/<int:id>/',views.EditProduct, name='edit_product'), 
    path('delete_product/<int:id>/',views.DeleteProduct, name='delete_product'), 

    path('category_list/',views.CategoryList,name='category_list'),
    path('add_category/',views.AddCategory, name='add_category'),
    path('edit_category/<int:id>/',views.EditCategory, name='edit_category'),
    path('delete_category/<int:id>/',views.DeleteCategory, name='delete_category'),  


    path('variation_list/',views.VariationList,name='variation_list'),
    path('add_variation/',views.AddVariation, name='add_variation'),
    path('edit_vatiation/<int:id>/',views.EditVariation, name='edit_vatiation'),
    path('delete_variation/<int:id>/',views.DeleteVariation, name='delete_variation'),  

    path('orders/', views.orders,name='orders'),
    path('order_details/<int:id>/', views.orderdetails, name='order_details'),
    path('update_order/<int:pk>/', views.update_order_status, name='update_order')
]