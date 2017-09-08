from django.conf.urls import url
from django.contrib import admin

from .views import (
    ShipperListAPIView,
    ShipperDetailAPIView,
    ShipperCreateAPIView,
    ShipperDeleteAPIView
    )

urlpatterns = [
	url(r'^$', ShipperListAPIView.as_view(), name='list'),
	url(r'^create/$', ShipperCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', ShipperDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', ShipperDeleteAPIView.as_view(),name='delete'),
 
]