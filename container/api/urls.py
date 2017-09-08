from django.conf.urls import url
from django.contrib import admin

from .views import (
    ContainerListAPIView,
    ContainerDetailAPIView,
    ContainerCreateAPIView,
    ContainerDeleteAPIView
    )

urlpatterns = [
	url(r'^$', ContainerListAPIView.as_view(), name='list'),
	url(r'^create/$', ContainerCreateAPIView.as_view(),name='create'),
	url(r'^(?P<number>[\w-]+)/$', ContainerDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<number>[\w-]+)/delete/$', ContainerDeleteAPIView.as_view(),name='delete'),
 
]