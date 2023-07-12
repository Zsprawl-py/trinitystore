from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import Order
from shop.models import Product


@require_POST
def create_order(request, ):
    now = datetime.now()
    form = request.POST
    form = form['plan']
    product = get_object_or_404(Product, plan_type=form)
    user = request.user
    order = Order.objects.create(user=user, item=product, price=product.price)
    order.save()
    request.session['order_id'] = order.id
    return render(request, 'order/order.html', {'order': order, "product": product, "user": user, 'now': now})


def apple(request):
    pass
