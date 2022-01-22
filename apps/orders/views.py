from django.shortcuts import render

from apps.cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity']
                )
            # clear the cart 
            cart.clear()
            # launch asychronous task
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order, 'cart': cart})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
