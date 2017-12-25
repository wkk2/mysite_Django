from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import User,ConfirmString
from .forms import UserForm,RegisterForm
import hashlib
import datetime
from django.core.mail import EmailMultiAlternatives
from mysite_use_virtualenv import settings

def index(request):
    return render(request,'index.html')

def register(request):
    if request.session.get('is_login',None):
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = 'Please check all fields'
        if register_form.is_valid():
            name = register_form.cleaned_data['name']
            password = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password != password2:
                message = 'The passwords are not equal'
                return render(request, 'register.html', {'form': register_form, 'message': message})
            user = User.objects.filter(name=name)
            if user:
                message ='The user name is already exist'
                return render(request, 'register.html', {'form': register_form, 'message': message})
            '''
            user = User.objects.filter(email=email)
            if user:
                message = 'The email is already registed'
                return render(request, 'register.html', {'form': register_form, 'message': message})
          '''
            new_user = User.objects.create()
            new_user.name = name
            new_user.password = hash_code(password)
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            code = make_confirm_string(new_user)
            send_email(email,code)
            return HttpResponseRedirect('/login/')
        return render(request,'register.html',{'form':register_form,'message':message})
    form = RegisterForm()
    return render(request,'register.html',{'form':form})


def login(request):
    if request.session.get('is_login',None):
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        print(login_form)
        message = "Username and Password are required!"
        print(login_form.is_valid())
        if login_form.is_valid():
            print('---')
            name = login_form.cleaned_data['name']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=name)
                if user.has_confirmed == False:
                    message = 'Have not confirmed!'
                    return render(request,'login.html',locals())
                if hash_code(password) == user.password:
                    request.session['is_login'] = True
                    request.session['user'] = user.name
                    request.session['password'] = user.password
                    return HttpResponseRedirect('/index/')
                else:
                    message = 'Password is wrong!'
            except:
                message = 'This user is not registered!'
        return render(request, 'login.html', locals())
    return render(request, 'login.html',{'login_form':UserForm()})



def logout(request):
    if not request.session.get('is_login',None):
        return render(request,'index.html')
    request.session.flush()
    return render(request,'index.html')

def hash_code(s,salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name,now)
    ConfirmString.objects.create(code=code,user=user)
    return code

def send_email(email,code):
    subject = 'welcome register'
    text_content = 'message:aaa'
    html_content = '''<p>blog:<a href="http://{}/confirm/?code={}" target="blank">ljBlog</a></p>
                    <p>此链接有效期为{}天'''.format('127.0.0.1:8000',code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email], )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def user_confirm(request):
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = 'Invalid request!'
        return render(request,'login/confirm.html',locals())
    register_time = confirm.register_time
    register_time = register_time.replace(tzinfo=None)
    now = datetime.datetime.now()
    if now > register_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())