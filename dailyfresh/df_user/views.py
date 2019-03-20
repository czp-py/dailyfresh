# coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from .models import *
from df_goods.models import *
from df_cart.models import *
from df_order.models import *
from hashlib import sha1
from . import user_decorator
from django.core.paginator import Paginator

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
            # 记录登陆前的页面
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 是否勾选记住用户选项
            if remember != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            # 在session中存储用户信息
            cart_count = CartInfo.objects.filter(user_id=int(users[0].id)).count()
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            request.session['cart_count'] = cart_count
            return red
        else:
            context = {'title':'天天生鲜-登陆', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '天天生鲜-登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


# 用户中心-个人信息页
@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    # 浏览记录
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    print(goods_ids1)
    for goods_id in goods_ids1:
        if goods_id != '':
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context={
        'title': '天天生鲜-用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'page_name': 1,
        'goods_list': goods_list
    }
    return render(request, 'df_user/user_center_info.html', context)


# 用户中心-订单页
@user_decorator.login
def order(request, oindex):
    user_id = request.session['user_id']
    orderinfos = list(OrderInfo.objects.filter(user_id=user_id))
    i = 0
    for orderinfo in orderinfos:
        orderinfos[i]=[orderinfos[i],OrderDetailInfo.objects.filter(order_id=orderinfo.oid)]
        i += 1
    print(orderinfos)
    # 分页处理
    paginator = Paginator(orderinfos, 5)
    page = paginator.page(int(oindex))
    context = {'title':'天天生鲜-用户中心', 'orderinfos': orderinfos, 'page': page, 'paginator': paginator}
    return render(request, 'df_user/user_center_order.html/', context)


# 用户中心-收货地址页
@user_decorator.login
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


