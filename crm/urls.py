"""crm URL Configuration

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
# from django.conf.urls import url
# from django.contrib import admin
# from django.conf.urls import include, url
# from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shore/', include('shore.urls')),
    url(r'api/booking/', include("shore.api.urls", namespace='booking-api')),
    url(r'api/shipper/', include("shipper.api.urls", namespace='shipper-api')),
    url(r'api/vessel/', include("vessel.api.urls", namespace='vessel-api')),
    url(r'api/container/', include("container.api.urls", namespace='container-api')),
    url(r'api/shorefile/', include("shorefile.api.urls", namespace='shorefile-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
