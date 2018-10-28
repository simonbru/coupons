from typing import List, Union

from django.db.models import QuerySet
from django.utils.functional import lazy

from .models import Coupon


def list_of_unique_coupon_titles() -> Union[QuerySet, List[str]]:
    return (
        Coupon
        .objects
        .order_by()  # Clear ordering for "distinct" to work
        .values_list('title', flat=True)
        .distinct()
    )


lazy_list_of_unique_coupon_titles = lazy(list_of_unique_coupon_titles, List[str])
