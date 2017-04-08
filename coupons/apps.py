from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class CouponsConfig(AppConfig):
    name = 'coupons'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
