from django.db import models


# Create your models here.
# 用户中心的订单信息，没无法实现真实支付，物流信息
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oadress = models.CharField(max_length=100)
    user = models.ForeignKey('df_user.UserInfo')


# 订单详情
class OrderDetailInfo(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 小计
    count = models.IntegerField()
    order = models.ForeignKey(OrderInfo)
    goods = models.ForeignKey('df_goods.GoodsInfo')