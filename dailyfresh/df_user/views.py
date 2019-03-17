# coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from .models import *
from hashlib import sha1

# Create your views here.


# 注册页面
def register(request):
    title = {'title':'天天生鲜-注册'}
    return render(request, 'df_user/register.html', title)


# 注册时检查用户名是否存在
def register_exit(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


# 注册处理
def register_handle(request):
    # 接收注册用户提交的数据信息
    post = request.POST
    uname = post.get('user_name')  # 用户名
    upwd = post.get('pwd')  # 密码
    cpwd = post.get('cpwd')  # 第二次输入的密码
    uemail = post.get('email')  # 电子邮箱
    # 判断两次密码是否相同
    if upwd != cpwd:
        return redirect('user/register/')
    # 对密码进行加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd2 = s1.hexdigest()
    # 创建新用户
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail
    user.save()
    # 注册后转到登陆界面
    return redirect('/user/login/')


# 登陆页面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'天天生鲜-登陆', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html',context)


# 登陆处理
def login_handle(request):
    # 接收信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # 判断是否存在用户，存在用户再判断密码是否正确，然后转向用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        # 判断密码是否正确
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # 是否勾选记住用户选项
            if remember != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            # 在session中存储用户信息
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title':'天天生鲜-登陆', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '天天生鲜-登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


# 用户中心-个人信息页
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context={
        'title':'天天生鲜-用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name']
    }
    return render(request, 'df_user/user_center_info.html', context)


# 用户中心-订单页
def order(request):
    context = {'title':'天天生鲜-用户中心'}
    return render(request, 'df_user/user_center_order.html/', context)


# 用户中心-收货地址页
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.urece = post.get('urece')
        user.uadress = post.get('uadress')
        user.upost = post.get('upost')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'天天生鲜-用户中心', 'user':user}
    return render(request, 'df_user/user_center_site.html', context)


