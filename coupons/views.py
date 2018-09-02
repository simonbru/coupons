import itertools

import barcode
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

from .utils import parse_geoloc_coords
from .forms import CommentForm
from .models import Coupon


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
            'title': 'Tous les bons',
            'by_category': self.coupons_by_category(),
        }


class RecentCouponListView(CouponListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(featured=True)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'title': 'Bons du moment',
        }


class CouponDetailView(DetailView):
    model = Coupon
    comment_form: CommentForm

    def get(self, request, *args, **kwargs):
        self.comment_form = CommentForm(initial={
            'restaurant': request.session.get('last_restaurant', None),
        })

        # Sort restaurants using coordinates given in cookies
        coords_cookie = request.COOKIES.get('coords')
        if coords_cookie:
            try:
                coords = parse_geoloc_coords(coords_cookie)
            except ValueError as e:
                print("Warning: Could not parse geoloc coordinates.", e)
            else:
                self.comment_form.sort_restaurants_by_distance(
                    coords['lat'], coords['lon']
                )
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
                "Votre note a bien été pris en compte."
            )
            request.session['last_restaurant'] = comment.restaurant_id
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
        barcode_svg = (
            barcode
            .Code128(coupon.barcode)
            .render({'text': coupon.barcode})
        )
        return HttpResponse(
            barcode_svg, content_type='image/svg+xml'
        )
