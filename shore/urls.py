"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$upload', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url

from .views import upload,import_data,confirm_data,delete_data,index,daily,export_booking_csv

urlpatterns = [
    url(r'^$',import_data ,name=''),
    url(r'^report/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',daily ,name='daily'),
    url(r'^report/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',index ,name='monthly'),
    url(r'^report/$',index ,name='index'),
    url(r'^confirm/$',confirm_data ,name='confirm'),
    url(r'^delete/$',delete_data ,name='delete'),
    url(r'^csv/$',export_booking_csv ,name='export_csv'),
]
