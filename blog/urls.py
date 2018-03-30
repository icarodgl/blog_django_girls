from django.conf.urls import url
from django.urls import path, re_path, include
from . import views
from django.contrib.auth.forms import  *

urlpatterns = [
    re_path(r'^$',views.post_list, name='post_list'),
    re_path(r'^home/$',views.post_list, name='post_list'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    re_path('acconts/', include('django.contrib.auth.urls'),name='contas'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path('logout/', views.logout, name='logout'),
    re_path('profile/',views.profile, name='profile'),
]
