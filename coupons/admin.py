from django import forms
from django.contrib import admin

from .forms import TextInputWithAutocomplete
from .models import Coupon, Category, Restaurant, Comment
from .services import lazy_list_of_unique_coupon_titles


class CouponForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': TextInputWithAutocomplete(
                choices=lazy_list_of_unique_coupon_titles(),
                attrs={
                    'size': 50,
                }
            ),
        }


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    form = CouponForm
    list_display = ['title', 'category', 'price', 'barcode', 'created_at', 'featured', 'display_active']
    search_fields = ['title', 'barcode']
    list_editable = ['featured']
    save_as = True

    def display_active(self, obj=None):
        return obj and not obj.disabled

    display_active.boolean = True
    display_active.short_description = 'actif'
    display_active.admin_order_field = 'disabled'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_address', 'city', 'lat', 'lon']
    search_fields = ['address', 'name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'does_coupon_work', 'coupon', 'restaurant', 'author_ip']
