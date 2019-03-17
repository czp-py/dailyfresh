# coding=utf-8
from django.db import models
from tinymce.models import HTMLField


# Create your models here.
# 商品类型
class TypeInfo(models.Model):
    tname = models.CharField(max_length=20)  # 分类名称
    isDelete = models.BooleanField(default=False)  # 逻辑删除

    def __str__(self):
        return self.tname


# 商品模型
class GoodsInfo(models.Model):
    gname = models.CharField(max_length=20)  # 商品名称
    gpic = models.ImageField(upload_to='df_goods')  # 商品图片
    gprice = models.DecimalField(max_digits=5, decimal_places=2)  # 商品价格
    gunit = models.CharField(max_length=20)  # 单位
    gclick = models.IntegerField()  # 商品点击查看次数
    gintro = models.CharField(max_length=200)  # 商品简介
    gcontent = HTMLField()  # 商品的具体描述
    gstock = models.IntegerField()  # 库存
    # gadv = models.BooleanField(default=False)  # 推荐
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    gtype = models.ForeignKey(TypeInfo)  # 外键

    def __str__(self):
        return self.gname
