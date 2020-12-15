from django.urls import path
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.home, name='index'),
    path('login/', views.login_service, name='login'),
    path('logout/', views.logout_service, name='logout'),
    path('applypair/', views.pair, name='applypair'),
    path('convalidation/', views.convalidate, name='convalidation'),
    path('convalidation_help/', views.convalidate_help,
         name='convalidation_help'),
    path('applygroup/', views.group, name='applygroup'),
    path('group_help/', views.group_help, name='group_help'),
    path('login_help/', views.login_help, name='login_help'),
    path('pair_help/', views.pair_help, name='pair_help'),
    path('breakpair/', views.breakpair, name='breakpair')
]
