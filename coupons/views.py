import barcode
import itertools
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.views.generic.detail import SingleObjectMixin
from ipware.ip import get_ip

from .forms import CommentForm
from .models import Coupon, Category


class FirstView(TemplateView):
    template_name = 'base.html'


class CouponListView(ListView):
    model = Coupon

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_anonymous:
            return queryset.filter(disabled=False)
        else:
            return queryset

    def coupons_by_category(self):
        def keyfunc(coupon):
            return coupon.category_id
        coupons = sorted(self.get_queryset(), key=keyfunc)
        groups_list = [
            list(coupons) for category_id, coupons
            in itertools.groupby(coupons, key=keyfunc)
        ]
        return {
            coupons[0].category: coupons
            for coupons in groups_list
        }

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'by_category': self.coupons_by_category(),
        }


class CouponDetailView(DetailView):
    model = Coupon

    def get(self, request, *args, **kwargs):
        self.comment_form = CommentForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.comment_form = CommentForm(data=request.POST)
        if self.comment_form.is_valid():
            coupon = self.get_object()
            comment = self.comment_form.instance
            comment.coupon = coupon
            comment.author_ip = get_ip(request)
            comment.save()
            messages.success(
                request,
                "Votre commentaire a bien été pris en compte."
            )
            return redirect('coupon_detail', self.get_object().id)
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'comment_form': self.comment_form,
        }


class CouponBarcodeView(SingleObjectMixin, View):
    model = Coupon

    def get(self, request, *args, **kwargs):
        coupon = self.get_object()
        barcode_svg = barcode.EAN13(coupon.barcode).render()
        return HttpResponse(
            barcode_svg, content_type='image/svg+xml'
        )
