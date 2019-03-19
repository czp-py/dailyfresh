from django.db import models

# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo')  # 用户
    goods = models.ForeignKey('df_goods.GoodsInfo')  # 物品
    count = models.IntegerField()  # 购买的数量
