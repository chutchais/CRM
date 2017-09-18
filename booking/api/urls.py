from django.conf.urls import url
from django.contrib import admin

from .views import (
    BookingListAPIView,
    BookingDetailAPIView,
    BookingCreateAPIView,
    BookingDeleteAPIView
    )

urlpatterns = [
	url(r'^$', BookingListAPIView.as_view(), name='list'),
	url(r'^create/$', BookingCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', BookingDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', BookingDeleteAPIView.as_view(),name='delete'),
 
]