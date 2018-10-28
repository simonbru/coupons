from typing import Iterable, Optional

from django import forms
from django.contrib import admin

from .models import Coupon, Category, Restaurant, Comment
from .services import list_of_unique_coupon_titles


class TextInputWithAutocomplete(forms.TextInput):
    template_name = 'widgets/text_autocomplete.html'
    datalist_id: Optional[str]
    choices: Iterable[str]

    def __init__(self, *args, datalist_id=None, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.datalist_id = datalist_id
        self.choices = choices or []

    def get_datalist_id(self, attrs):
        """
        Generate datalist id from input id
        if `datalist_id` was not specified
        """
        if self.datalist_id is not None:
            datalist_id = self.datalist_id
        else:
            datalist_id = attrs.get('id', '') + '--datalist'
        return datalist_id

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('list', self.get_datalist_id(attrs))
        return attrs

    def get_context(self, name, value, attrs):
        return {
            **super().get_context(name, value, attrs),
            'choices': self.choices
        }


class CouponForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': TextInputWithAutocomplete(
                choices=list_of_unique_coupon_titles(),
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
