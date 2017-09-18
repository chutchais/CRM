from django.conf.urls import url
from django.contrib import admin

from .views import (
    ContainerListAPIView,
    ContainerDetailAPIView,
    ContainerCreateAPIView,
    ContainerDeleteAPIView,
    ContainerUpdateAPIView
    )

urlpatterns = [
	url(r'^$', ContainerListAPIView.as_view(), name='list'),
	url(r'^create/$', ContainerCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', ContainerDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', ContainerDeleteAPIView.as_view(),name='delete'),
	url(r'^(?P<slug>[\w-]+)/update/$', ContainerUpdateAPIView.as_view(),name='update'),
	# url(r'^dd/$', ContainerUpdateAPIView.as_view(),name='update'),
 ]

# ContainerDetailAPIView