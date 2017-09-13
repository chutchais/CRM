from django.conf.urls import url
from django.contrib import admin

from .views import (
    ShoreFileListAPIView,
    ShoreFileDetailAPIView,
    ShoreFileCreateAPIView,
    ShoreFileDeleteAPIView,
    ShoreFileUpdateAPIView
    )

urlpatterns = [
	url(r'^$', ShoreFileListAPIView.as_view(), name='list'),
	url(r'^create/$', ShoreFileCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', ShoreFileDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', ShoreFileDeleteAPIView.as_view(),name='delete'),
	url(r'^(?P<slug>[\w-]+)/update/$', ShoreFileUpdateAPIView.as_view(),name='update'),
 
]