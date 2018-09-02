import json
import numbers
import urllib
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import mail_managers
from django.shortcuts import resolve_url
from django.utils.html import format_html


def parse_geoloc_coords(cookietext):
    try:
        jsontext = urllib.parse.unquote(cookietext)
        coords = json.loads(jsontext)
    except json.JSONDecodeError as e:
        raise ValueError(e)

    if not (
        isinstance(coords.get('lat'), numbers.Number) and
        isinstance(coords.get('lon'), numbers.Number)
    ):
        raise ValueError("lat and lon must be numbers")

    return coords


def send_warning_for_coupon(coupon, comment):
    coupon_url = urljoin(settings.BASE_URL, resolve_url(coupon))
    coupon_admin_url = urljoin(
        settings.BASE_URL,
        resolve_url('admin:coupons_coupon_change', object_id=coupon.id),
    )

    subject = f'Signalement du bon pour "{coupon.title}"'

    body = """
Le bon pour "{coupon_title}" a été signalé comme non-fonctionnel
au restaurant "{restaurant}", alors qu'il est affiché dans les bons du moment.

Voir le bon: {coupon_url}

Voir le bon dans l'admin: {coupon_admin_url}
"""

    body_html = """
<p>
    Le bon pour
    <a href="{coupon_url}">{coupon_title}</a> a été signalé comme non-fonctionnel
    au restaurant "{restaurant}", alors qu'il est affiché dans les bons du moment.
</p>
<p>
    <a href="{coupon_admin_url}">Voir le bon dans l'admin</a>
</p>
"""

    render_context = dict(
        coupon_url=coupon_url,
        coupon_admin_url=coupon_admin_url,
        coupon_title=coupon.title,
        restaurant=comment.restaurant,
    )
    mail_managers(
        subject,
        message=body.format(**render_context),
        html_message=format_html(body_html, **render_context),
        fail_silently=True
    )
