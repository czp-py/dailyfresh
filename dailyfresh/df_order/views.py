from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from df_cart.models import *
from django.db import transaction
from .models import *
from datetime import datetime
from decimal import Decimal


# Create your views here.


@user_decorator.login
def order(request):
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    for cart_id in cart_ids:
        carts.extend(CartInfo.objects.filter(id=int(cart_id)))
    context = {'title': '天天生鲜-提交订单', 'page_name': '2', 'carts': carts}
    return render(request, 'df_order/order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.POST.getlist('cart_id')
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal =Decimal(request.POST.get('total'))
        order.save()
        # 创建详细订单对象
        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gstock >= cart.count:  # 如果库存大于购买数量
                # 减少商品库存
                goods.gstock =cart.goods.gstock-cart.count
                goods.save()
                # 完善详细订单信息
                detail.goods_id = goods.id
                detail.count = cart.count
                detail.price = goods.gprice * detail.count
                detail.save()
                # 删除购物车内的信息
                cart.delete()
                request.session['cart_count'] -= 1
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("=================%s"%e)
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/1/')