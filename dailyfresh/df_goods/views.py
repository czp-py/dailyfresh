from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

# Create your views here.

# 首页
def index(request):
    typelist = TypeInfo.objects.all()
    # 查询各分类最新、点击量最多的数据信息
    type0_new = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type0_most = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1_new = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type1_most = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2_new = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type2_most = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3_new = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type3_most = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4_new = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type4_most = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5_new = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type5_most = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title':'天天鲜-首页', 'guest_cart':1,
               'type0_new': type0_new, 'type0_most': type0_most,
               'type1_new': type1_new, 'type1_most': type1_most,
               'type2_new': type2_new, 'type2_most': type2_most,
               'type3_new': type3_new, 'type3_most': type3_most,
               'type4_new': type4_new, 'type4_most': type4_most,
               'type5_new': type5_new, 'type5_most': type5_most,}
    return render(request, 'df_goods/index.html', context)


# 商品列表页，其中tid分类编号， pindex页数， sort排序方式
def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    newgoods = typeinfo.goodsinfo_set.order_by('-id')[0:2]  # 新品推荐
    if sort == '1':  # 1为默认，显示最新的商品
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # 2为价格排序
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # 3为点击量（人气）排序
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    # 分页处理
    paginator = Paginator(goodslist, 10)
    page = paginator.page(int(pindex))
    context={
        'title': '天天鲜-商品列表',
        'tname': typeinfo.tname, 'guest_cart': 1,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'newgoods': newgoods
    }
    return render(request, 'df_goods/list.html', context)


# 商品详细页
def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick += 1 #点击量增加
    goods.save()
    newgoods = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': '天天鲜-商品详细信息','gname': goods.gname,
        'guest_cart': 1,'g': goods, 'newgoods': newgoods, id: 'id'
    }
    response = render(request, 'df_goods/detail.html', context)

    # 记录最近浏览的商品，在用户中心显示
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d'%goods.id
    # 判断是否有浏览记录
    if goods_id != '':
        goods_ids1 = goods_ids.split(',')  # 拆分
        # 判断id是否存在
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)  # 添加到第一个
        # 判断id是否超过六个
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)  # 拼接
    else:
        goods_ids = goods_id  # 如果没有就直接添加
    response.set_cookie('goods_ids', goods_ids)  # 写入cookie

    return response