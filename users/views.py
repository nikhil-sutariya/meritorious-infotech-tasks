from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import get_template
from users.models import User
from django.contrib.auth.decorators import login_required
from users.utils import Utils

@login_required(login_url="/login")
def home(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

def signup(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            phone = request.POST['phone']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1==password2: 
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already registered.')
                    return redirect('signup')
                if User.objects.filter(phone=phone).exists():
                    messages.error(request, 'This phone number is already registered.')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(email=email, phone=phone, password=password1)
                    user.save()
                    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                    token = PasswordResetTokenGenerator().make_token(user)
                    current_site = get_current_site(request=request).domain
                    relative_link = reverse('verify_user', kwargs={'uidb64': uidb64, 'token': token})
                    absurl = f'http://{current_site}{relative_link}?token={str(token)}'

                    context = {
                        "email": email,
                        "url": absurl
                    }

                    email_body = get_template('email_templates/verification-mail.html').render(context)
                    data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
                    Utils.send_email(data)

                    messages.success(request, 'Signup completed and we have sent you a account verification link to verify you account.')
                    return redirect('login')
            else:
                messages.success(request, 'Password and confirm password must be same.')
                return redirect('signup')

        return render(request, 'signup.html')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

def verify_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)

        if PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            messages.success(request, 'Your email has been verified. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'The verification link is invalid or has expired.')
            return redirect('signup')
        
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('signup')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong, please try again later!</body></html>')

def login_view(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if not user.is_email_verified:
                messages.error(request, 'Please verify your account first')
                return redirect('login')

            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request, 'login.html')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')
    
def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'You are successfully logged out!')
        return redirect('login')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required(login_url="/login")
def profile(request):
    try:
        user = request.user
        if request.method == 'POST':
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            is_any_errors = False

            if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, 'This email is already taken by another user.')
                is_any_errors = True

            if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, 'This email is already taken by another user.')
                is_any_errors = True

            if is_any_errors:
                return render(request, 'profile.html', {'user': user})

            user.phone = phone
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')

        return render(request, 'profile.html', {'user': user})
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required(login_url="/login")
def admin_panel(request):
    try:
        if not request.user.is_superuser:
            messages.success(request, 'Only admin users can access this page')
        return render(request, 'admin_panel.html')
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')
