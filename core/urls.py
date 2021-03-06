from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('create/', include('apps.orders.urls', namespace='orders')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
    path('coupons/', include('apps.coupons.urls', namespace='coupons')),
    path('', include('apps.shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
