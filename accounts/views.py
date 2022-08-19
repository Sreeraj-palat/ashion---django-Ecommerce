from http.client import HTTPResponse
from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from .forms import RegistrationForm, VerifyForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import verify
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator    
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.forms import ValidationError
from carts.views import _cart_id
import requests




# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            user.phone_number = phone_number #not given the phone_number feild in models(create_user). thats why phone number is saved like this
            request.session['phone_number'] = phone_number
            print(phone_number)
            user.save()
            verify.send(form.cleaned_data.get('phone_number'))
            messages.success(request,'Registration is successfull')
            return redirect('verify')            
            
    else:
        form = RegistrationForm()

    context = {
        'form' : form,
    }
    return render(request,'register.html', context)





def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')




@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = request.session['phone_number']
            if verify.check(phone, code):
                user = Account.objects.get(phone_number = phone)
                user.is_active = True
                user.save()
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})



def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            

            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your password'
            message = render_to_string('reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.SUCCESS(request,'password reset email has been sent to your email ')
            return redirect('login')


        else:
            messages.error(request,'Account does not exist')   
            return redirect('forgotpassword') 
    return render(request, 'forgotpassword.html')    




def resetpassword_validate(request):
    return HTTPResponse('ok')



