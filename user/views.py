from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login,authenticate
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text
from django.core.mail import EmailMessage
from .forms import UserForm
from .models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def login(request):
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True
        username = request.POST.get('username')
        try:
            check=User.objects.get(username=username)
        except:
            check=None
        if check is not None:
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                
                auth_login(request, user)
                return redirect("http://127.0.0.1:8000")
            else:
                messages.error(request,'please re-check your password')
                return render(request,'login/index.html')
        else:
            messages.error(request, 'Username doesnot exist')
            return render(request, 'login/index.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'login/index.html')

    return render(request,'login/index.html')

def signup(request):
    if request.method =='POST':
        storage = messages.get_messages(request)
        storage.used = True
        user_form = UserForm(request.POST)
        if request.POST.get('password') == request.POST.get('confirm_password'):
            email = request.POST.get('email')
            try:
                email_check = User.objects.get(email=email) 
            except:
                email_check = None
            if email_check is None:

                username = request.POST.get('username')
                try:
                    username_check = User.objects.get(username=username)
                except:
                    username_check = None
                if username_check is None:

                    if user_form.is_valid():
                        user = user_form.save(commit=False)
                        user.set_password(user.password)
                        user.save()
                        return render(request,'login/index.html')
                    else:
                        messages.error(request, 'Invalid Submission')
                        return render(request, 'login/signup.html', {'user_form': user_form})
                else:
                    messages.error(request, 'Username already exists')
                    return render(request, 'login/signup.html', {'user_form': user_form})
            else:
                messages.error(request, 'Email already exists')
                return render(request, 'login/signup.html', {'user_form': user_form})
        else:
            messages.error(request, 'passwords do not match')
            return render(request, 'login/signup.html', {'user_form': user_form})
    else:
        storage = messages.get_messages(request)
        storage.used = True
        user_form = UserForm()
        return render(request, 'login/signup.html', {'user_form': user_form})



        

    

def forgot(request):
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True
    return render(request,'login/forgot.html')
@login_required
def logout(request):
    django_logout(request)
    return render(request,'login/index.html')