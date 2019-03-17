# coding=utf-8
from django.db import models


# Create your models here.
# 用户信息模型
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)  # 用户名
    upwd = models.CharField(max_length=40)  # 密码
    uemail = models.CharField(max_length=30)  # 邮箱
    urece = models.CharField(max_length=20, default='')  # 收件人姓名
    uadress = models.CharField(max_length=100, default='')  # 收件地址
    upost = models.CharField(max_length=6, default='')  # 邮编
    uphone = models.CharField(max_length=11, default='')  # 电话
