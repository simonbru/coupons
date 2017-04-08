from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)

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
