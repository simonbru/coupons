from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from coupons.models import Category


class FirstView(TemplateView):
    template_name = 'base.html'


class CouponListView(ListView):
    model = Category
    template_name = 'coupons/coupon_list.html'
    context_object_name = 'categories'
