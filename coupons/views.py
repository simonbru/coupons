import barcode
from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.views.generic.detail import SingleObjectMixin

from coupons.models import Coupon, Category


class FirstView(TemplateView):
    template_name = 'base.html'


class CouponListView(ListView):
    model = Coupon

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'categories': Category.objects.all(),
        }


class CouponDetailView(DetailView):
    model = Coupon


class CouponBarcodeView(SingleObjectMixin, View):
    model = Coupon

    def get(self, request, *args, **kwargs):
        coupon = self.get_object()
        barcode_svg = barcode.EAN13(coupon.barcode).render()
        return HttpResponse(
            barcode_svg, content_type='image/svg+xml'
        )
