from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from .forms import Login, PasswordReset, Signup, Change, Reset
from .models import UserModels, ResetPassword
from secrets import choice, token_urlsafe
from string import hexdigits
from django.contrib.auth.hashers import make_password, check_password, MD5PasswordHasher
from django.contrib.auth import login as _login
from django.db import connection
from django.conf import settings
from functools import wraps
from django.urls import reverse
from datetime import datetime,timedelta

def login_required(func):
    @wraps(func)
    def login_verification(request, *args, **kwargs):
        user = request.user
        print(user.is_authenticated)
        if user.is_authenticated:
            return func(request,user=user,*args, **kwargs)
        else:
            return redirect(reverse(login))
    return login_verification

def generate_username(number=10):
    id = ''
    for len in range(number):
        id += choice(hexdigits)
    return id

def signup(request):
    signup_form = Signup()
    post_info = request.POST
    if post_info:
        validate = Signup(post_info)
        if not validate.is_valid():
            return HttpResponse(validate.errors.as_ul())
        
        password = make_password((post_info.get('password')))

        UserModels.objects.create(id=generate_username(), email=post_info.get('email'), name=post_info.get('name'), password=password)
        return HttpResponse('Account Created, You can now login at ...')
    return render(request, 'signup.html', {'form': signup_form })


def login(request):
    login_form = Login()
    post_info = request.POST
    
    if post_info:

        validate = Login(post_info)
        if not validate.is_valid():
            return HttpResponse(validate.errors.as_ul())

        else:
            email = post_info.get('email')
            password = post_info.get('password')
            check_user = UserModels.objects.filter(email=email).select_related()
            content = check_user.values()

            if content:
                password_valid = check_password(password, content[0].get('password')) # type: ignore
                if password_valid:
                    _login(request,user=check_user.get())
                    # print(len(connection.queries))
                    redirect_url = getattr(settings, 'LOGIN_REDIRECT', '/')
                    # return None
                    return  HttpResponse(status=204, headers={'HX-Redirect': redirect_url})
                else:
                    return HttpResponse('Password invalid try again')
            else:
                return HttpResponse('Try again user do not exist')

    return render(request, 'login.html', {'form': login_form })
    
@login_required
def change_password(request, user=None):
    change_form = Change()
    
    post_info = request.POST
    if post_info:
        validate = Change(post_info)
        if not validate.is_valid():
            return HttpResponse(validate.errors.as_ul())
        
        data = validate.data
        old_password = data.get('Old_Password')
        new_password = data.get('New_Password')
        password_again = data.get('New_Password_Again')
        
        
        if old_password == new_password:
            return HttpResponse('<ul><li>  Old Pasword & New Password <ul class="errorlist"><li>Old password and New password should be different </li> </ul></li></ul>')
        if new_password != password_again:
            return HttpResponse('<ul><li>  New Password & New Password Again <ul class="errorlist"><li>Old password and New password should be the same </li> </ul></li></ul>')

        filter = UserModels.objects.get(id=user.id) # type: ignore
        if check_password(old_password, filter.password):
            filter.password = make_password(new_password)
            filter.save()
            return HttpResponse('Password Changed you have to log in again')
        else:
            return HttpResponse('<ul><li>  Old Password <ul class="errorlist"><li>Old password is incorrect try again or reset password </li> </ul></li></ul>')



    return render(request, 'change_password.html', {'form': change_form })
    

def reset_password(request):
    reset_form = Reset()
    post_info = request.POST

    if post_info:
        validate = Reset(post_info)
        if not validate.is_valid():
            return HttpResponse(validate.errors.as_ul())
        
        email = post_info.get('Email')
        exist = UserModels.objects.filter(email=email)
        if not exist:
            return HttpResponse('<ul><li>  Email <ul class="errorlist"><li> There is no user with this email please try again </li> </ul></li></ul>')
        
        # create reset password token
        secret_token = token_urlsafe(16)
        RESET_TIME = getattr(settings, 'RESET_TIME', 10)
        time_range = RESET_TIME

        token = MD5PasswordHasher().encode(password=secret_token, salt='secrettoken')
        user = exist.get()
        time = datetime.now() + timedelta(minutes=time_range)
        
        print(secret_token, user)

        ResetPassword.objects.create(user_id=user, token=token, end_time=time)

        print(len(connection.queries))
        # send email with token
        return HttpResponse('Check you email you have the link to change your password')
    
    return render(request, 'reset_password.html', {'form': reset_form })


def reset(request, Token=None):
    filter,valid = ResetPassword.objects.validate(Token) # type: ignore
    user = ''
    if filter:
        user = filter.values()[0].get('user_id_id')
    print(user, valid)

    post_info = request.POST
    if post_info and valid:
        validate = PasswordReset(post_info)
        if not validate.is_valid():
            return HttpResponse(validate.errors.as_ul())
        new_password = post_info.get('New_Password')
        password_again = post_info.get('Password_Again')

        if new_password != password_again:
            return HttpResponse('<ul><li>  New Password & New Password Again <ul class="errorlist"><li>Old password and New password should be the same </li> </ul></li></ul>')
        
        UserModels.objects.filter(id=user).update(password=make_password(new_password))
        
        filter.delete()
        redirect_url = getattr(settings, 'RESET_REDIRECT', reverse(login))
        return HttpResponse(status=204, headers={'HX-Redirect': redirect_url})
    if user:
        if valid:
            password_reset = PasswordReset()
            return render(request, 'reset.html', {'form': password_reset, 'token':Token})
        else:
            return HttpResponse('Url expired you have to get another one')
    

    return HttpResponse('Try with a different token')
    
@login_required
def delete(request, user):
    user.delete()
    logout(request)
    return HttpResponse('done')


@login_required
def logout(request, user=None):
    request.session.flush()
    redirect_url = getattr(settings, 'LOGOUT_REDIRECT', '/') 
    return redirect(redirect_url)
    