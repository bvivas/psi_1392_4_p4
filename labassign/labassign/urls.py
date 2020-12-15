"""labassign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
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
    path('breakpair/', views.breakpair, name='breakpair'),
    path('core/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
