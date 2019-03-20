from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^register_exit', views.register_exit),
    url(r'^register_handle/$', views.register_handle),
    url(r'^login_handle/$', views.login_handle),
    url(r'^logout/$', views.logout),
    url(r'^info/$', views.info),
    url(r'^order/(\d+)/$', views.order),
    url(r'^site/$', views.site),
]