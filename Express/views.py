from . import forms
from . import models
from .plugins.sendcloud import sendtemplate

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from APP import settings

import os
import pytz
import hashlib
import datetime


def hash_code(s, salt='dingling'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def index(request):
    return render(request, 'Express/index.html')


def homepage(request):
    return render(request, 'Express/homepage.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/express')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        print(login_form)
        message = '所有的字段都必须填写！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在'
                return render(request, 'Express/login.html', locals())
            if not user.has_confirmed:
                message = '该用户还未通过邮件确认！不能登录！'
                return render(request, 'Express/login.html', locals())

            if user.password == password:  # hash_code(password)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/express')
            else:
                message = '密码错误'
                return render(request, 'Express/login.html', locals())
        else:
            return render(request, 'Express/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'Express/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('Express/')

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写项'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不相同！'
                return render(request, 'Express/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在，请重新选择！'
                    return render(request, 'Express/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已经被注册，请使用别的邮箱！'
                    return render(request, 'Express/register.html', locals())


            new_user = models.User()
            new_user.name = username
            # new_user.password = hash_code(password2)
            new_user.password = password2
            new_user.email = email
            new_user.sex = sex
            new_user.save()

            code = make_confirm_string(new_user)
            sendtemplate(email, username, 'https://' + os.environ['SERVER_NAME'] + '/express/confirm/?code=' + code)

            message = '请前往注册邮箱，进行确认！'

            return render(request, 'Express/confirm.html', locals())
        else:
            pass
    register_form = forms.RegisterForm()
    return render(request, 'Express/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/express/')
    request.session.flush()
    return redirect('/express/')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except Exception as e:
        print(e)
        message = '无效的请求！'
        return render(request, 'Express/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'Express/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'Express/confirm.html', locals())


def realname(request):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    '''
    exist_user = models.User.objects.get(pk=user_id)
    if request.method == 'POST':
        exist_user.verify = 1
        exist_user.save()
        control = 1
        return render(request, 'Express/realname.html', locals())

    control = exist_user.verify
    '''
    control = -1
    return render(request, 'Express/realname.html', locals())


def edit(request):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    exist_user = models.User.objects.get(pk=user_id)
    if exist_user.verify == -1:
        return redirect('/express/realname')
    if request.method == 'POST':

        user_id = request.session.get('user_id', None)

        express_number = request.POST.get('express_number', None)
        express_company = request.POST.get('express_company', None)
        express_height = request.POST.get('express_height', None)
        hurry_cost = request.POST.get('hurry_cost', None)
        height_cost = request.POST.get('height_cost', None)

        address = request.POST.get('address', None)
        latest_time = request.POST.get('latest_time', None)
        contact = request.POST.get('contact', None)
        tip_cost = request.POST.get('tip_cost', None)
        detail = request.POST.get('detail', None)

        hurry_cost = float(hurry_cost)
        height_cost = float(height_cost)
        tip_cost = float(tip_cost)
        express_height = int(express_height)

        exist_user = models.User.objects.get(pk=user_id)

        new_express = models.Express()
        new_express.pub_date = datetime.datetime.now()
        new_express.express_number = express_number
        new_express.express_company = express_company
        new_express.express_height = express_height
        new_express.hurry_cost = hurry_cost
        new_express.height_cost = height_cost
        new_express.address = address
        new_express.latest_time = latest_time
        new_express.contact = contact
        new_express.tip_cost = tip_cost
        new_express.detail = detail

        if hurry_cost >= 0 and height_cost >= 0 and tip_cost >= 0 and express_height >= 0:
            total = tip_cost + hurry_cost + 2.5 + express_height * 2.5
            if total >= 2.5:
                new_express.total_cost = total
                new_express.save()
                exist_user.save()
                new_express.publish_user.add(exist_user)
                return HttpResponseRedirect(reverse('Express:detail', args=(new_express.id,)))
        else:
            message = '请检查输入'
            render(request, 'Express/edit.html', locals())

    return render(request, 'Express/edit.html', locals())


def detail(request, express_id):
    user_id = request.session.get('user_id', None)
    if user_id != None:
        my_user = models.User.objects.get(pk=user_id)
    express = get_object_or_404(models.Express, pk=express_id)
    return render(request, 'Express/detail.html', locals())


def ground(request):
    express_all = models.Express.objects.all()
    return render(request, 'Express/ground.html', locals())


def detail_receive(request, express_id):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    exist_express = get_object_or_404(models.Express, pk=express_id)
    status = exist_express.status
    if status == 'publish':

        my_user = models.User.objects.get(pk=user_id)
        my_user.save()

        exist_express.receive_user.add(my_user)
        exist_express.status = 'receive'
        exist_express.receive_date = datetime.datetime.now()
        exist_express.save()

        control = 0
        return render(request, 'Express/detail_receive.html', locals())
    else:
        control = 1
        return render(request, 'Express/detail_receive.html', locals())


def detail_finish(request, express_id):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    exist_express = get_object_or_404(models.Express, pk=express_id)
    status = exist_express.status
    if status == 'receive':
        exist_express.status = 'finish'
        exist_express.finish_date = datetime.datetime.now()
        exist_express.save()
        control = 0
        return render(request, 'Express/detail_finish.html', locals())
    else:
        control = 1
        return render(request, 'Express/detail_finish.html', locals())


def detail_rate_receive(request, express_id):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    if request.method == 'POST':
        rate = request.POST.get('rate', None)
        exist_express = get_object_or_404(models.Express, pk=express_id)
        if rate != -1:
            exist_express.receive_user_rate = rate
            exist_express.save()
            control = 1
            return render(request, 'Express/detail_rate.html', locals())
        else:
            return render(request, 'Express/detail_rate.html', locals())
    control = 0
    return render(request, 'Express/detail_rate.html', locals())


def detail_rate_publish(request, express_id):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    if request.method == 'POST':
        rate = request.POST.get('rate', None)
        exist_express = get_object_or_404(models.Express, pk=express_id)
        if rate != -1:
            exist_express.publish_user_rate = rate
            exist_express.save()
            control = 1
            return render(request, 'Express/detail_rate.html', locals())
        else:
            return render(request, 'Express/detail_rate.html', locals())
    control = 0
    return render(request, 'Express/detail_rate.html', locals())


def my_receive(request):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)

    express_all = models.User.objects.get(pk=user_id).receive_user.all()
    return render(request, 'Express/my_receive.html', locals())


def my_publish(request):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)

    express_all = models.User.objects.get(pk=user_id).publish_user.all()
    return render(request, 'Express/my_publish.html', locals())


def my(request):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    my_user_id = request.session.get('user_id', None)
    if user_id == my_user_id:
        pass

    user = models.User.objects.get(pk=user_id)
    receive_express_all = user.receive_user.all()
    publish_express_all = user.publish_user.all()

    return render(request, 'Express/user.html', locals())


def user(request, user_id):
    if not request.session.get('is_login', None):
        message = '请先登录'
        return redirect('/express/login')
    user_id = request.session.get('user_id', None)
    my_user_id = request.session.get('user_id', None)
    if user_id == my_user_id:
        return redirect('/express/my')
    else:
        user = models.User.objects.get(pk=user_id)
        receive_all = user.receive_user.all()
        publish_all = user.publish_user.all()
        return render(request, 'Express/user.html', locals())


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自同村传递的注册确认邮件'

    text_content = '''感谢注册同村传递！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/express/confirm/?code={}" target=blank>同村传递</a>，\
                    <p>请点击“同村传递”完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(os.environ['SERVER_NAME'], code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
