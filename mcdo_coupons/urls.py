"""mcdo_coupons URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from coupons.views import (
    CouponListView,
    CouponDetailView,
    CouponBarcodeView,
    RecentCouponListView,
)

urlpatterns = [
    path('', lambda r: redirect('coupon_list'), name='index'),
    path('coupons/', CouponListView.as_view(), name='coupon_list'),
    path('recent-coupons/', RecentCouponListView.as_view(), name='recent_coupon_list'),
    path(
        'coupons/<int:pk>/',
        CouponDetailView.as_view(),
        name='coupon_detail'
    ),
    path(
        'coupons/<int:pk>/barcode/',
        CouponBarcodeView.as_view(),
        name='coupon_barcode'
    ),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
