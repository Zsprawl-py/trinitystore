import json

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from order.models import Order

from account.models import Subscribe

from actions.utils import create_action

from shop.models import Product


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
                user = order.user
                plan_type = order.item.plan_type
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            vip = Subscribe.objects.create(user=user, vip_type=plan_type)
            vip.remaining()
            create_action(user, 'has bought subscription', order)

    return HttpResponse(status=200)


def paypal_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        total = float(data['form']['total'])
        try:
            order = Order.objects.get(id=data['form']['order_id'])
        # user = User.objects.get(id=data['form']['user_id'])
        except Order.DoesNotExist:
            return HttpResponse(status=404)

        try:
            product = Product.objects.get(id=data['form']['product_id'])
        except Product.DoesNotExist:
            return HttpResponse(status=404)

        user = order.user
        if request.user != user:
            return HttpResponse(status=404)

        plan_type = product.plan_type
        order.paid = True
        order.save()
        vip = Subscribe.objects.create(user=user, vip_type=plan_type)
        vip.remaining()
        create_action(user, 'has bought subscription', order)

    return JsonResponse('Payment submitted..', safe=False)
