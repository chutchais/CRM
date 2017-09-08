from django.conf.urls import url
from django.contrib import admin

from .views import (
    BookingListAPIView,
    BookingDetailAPIView,
    BookingDeleteAPIView,
    PostCreateAPIView
    )

urlpatterns = [
	url(r'^$', BookingListAPIView.as_view(), name='booking_list'),
	url(r'^create/$', PostCreateAPIView.as_view(),name='create'),
	url(r'^(?P<number>[\w-]+)/$', BookingDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<number>[\w-]+)/delete/$', BookingDeleteAPIView.as_view(),name='delete'),
 # #    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
 #    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]