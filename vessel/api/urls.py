from django.conf.urls import url
from django.contrib import admin

from .views import (
    VesselListAPIView,
    VesselDetailAPIView,
    VesselCreateAPIView,
    VesselDeleteAPIView
    )

urlpatterns = [
	url(r'^$', VesselListAPIView.as_view(), name='list'),
	url(r'^create/$', VesselCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', VesselDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', VesselDeleteAPIView.as_view(),name='delete'),
 
]