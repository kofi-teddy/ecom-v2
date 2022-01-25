import braintree
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from apps.orders.models import Order
from .tasks import payment_completed

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = get_object_or_404()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', Nonce)
        # create and sumbmit transaction
        result = gateway.transaction.sale(
            {'amount': f'{total_cost:.2f}', 'payment_method_nonce': nonce, 'options': {'sumbmit_for_settlement': True}}
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # lunch asychronous tasks
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
