from django.contrib import admin

from coupons.models import Coupon, Category, Restaurant, Comment


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


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
