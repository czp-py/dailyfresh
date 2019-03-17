from django.contrib import admin
from .models import *
# Register your models here.


class adminTypeInfo(admin.ModelAdmin):
    list_display = ['id', 'tname']


class adminGoodsInfo(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gname', # 'gprice', 'gunit',
                    # 'gclick', 'gstock',
                    'gtype']


admin.site.register(TypeInfo, adminTypeInfo)
admin.site.register(GoodsInfo, adminGoodsInfo)