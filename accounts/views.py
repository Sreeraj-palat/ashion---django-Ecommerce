from django.shortcuts import render, redirect
from .forms import RegistrationForm, VerifyForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import verify
from django.views.decorators.csrf import csrf_exempt



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

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('home')

        else:
            messages.error(request,'invalid login credentials')   
            return redirect('login') 
    return render(request,'login.html')




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




