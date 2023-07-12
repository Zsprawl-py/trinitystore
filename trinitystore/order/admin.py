from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
        # return html
    return ''


order_payment.short_description = 'Stripe payment'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'price', 'created_time', 'paid', order_payment]
