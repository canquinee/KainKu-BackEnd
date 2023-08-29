from django.urls import re_path
from appTubesPI import views
from django.contrib import admin

urlpatterns = [
    re_path(r'^app/user(?:/(?P<lev>\b2\b|\b1\b|\b0\b))?/$', views.user_list),
    re_path(r'^app/user/profile/(?P<pk>[0-9]+)/$', views.user_detail),
    re_path(r'^app/user/create/$', views.user_create),
    re_path(r'^app/user/login/$', views.user_login),
    re_path(r'^app/user/logout/$', views.user_logout),

    re_path(r'^app/kain/$', views.kain_list),
    re_path(r'^app/kain/(?P<pk>[0-9]+)/$', views.kain_detail),

    re_path(r'^app/toko/$', views.toko_list),
    re_path(r'^app/toko/(?P<pk>[0-9]+)/$', views.listToko_detail),

    re_path(r'^app/toko/detail/$', views.detailToko_list),
    re_path(r'^app/toko/detail/(?P<pk>[0-9]+)/$', views.detailToko_detail),

    re_path('admin/', admin.site.urls),
]