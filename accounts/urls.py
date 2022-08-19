from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('verify/', views.verify_code, name='verify'),

    path('forgotpassword/', views.ForgotPassword, name='forgotpassword'),
    path('validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
]   