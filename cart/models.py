from django.db import models
from django.utils.translation import gettext_lazy as _
from . import constants as cart_constants


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(
        'users.User', on_delete=models.DO_NOTHING, related_name='carts')
    session = models.CharField(_('session'), max_length=255, blank=True, unique=True, help_text=_(
        'The unique session id associated with the cart.'))
    token = models.CharField(_('token'), max_length=255, blank=True, unique=True, help_text=_(
        'The unique token associated with the cart to identify the cart over multiple sessions. The same token can also be passed to the Payment Gateway if required.'))
    status = models.IntegerField(
        _('status'), choices=cart_constants.CART_STATUS_CHOICES, default=cart_constants.NEW)
    shipping_address = models.ForeignKey(
        'users.UserAddress', on_delete=models.DO_NOTHING, related_name='shipping_address', null=True, blank=True)
    billing_address = models.ForeignKey(
        'users.UserAddress', on_delete=models.DO_NOTHING, related_name='billing_address', null=True, blank=True)
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return self.product.name


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.DO_NOTHING, related_name='cart_items')
    sku = models.CharField(_('sku'), max_length=255, blank=True)
    quantity = models.IntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(
        'users.User', on_delete=models.DO_NOTHING, related_name='orders')
    cart = models.ForeignKey(
        Cart, on_delete=models.DO_NOTHING, related_name='orders')
    status = models.IntegerField(
        _('status'), choices=cart_constants.CART_STATUS_CHOICES, default=cart_constants.NEW)
    subtotal = models.DecimalField(
        _('subtotal'), max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(_('tax'), max_digits=10,
                              decimal_places=2, default=0)
    shipping_cost = models.DecimalField(
        _('shipping cost'), max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(
        _('total'), max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(_('grand total'), max_digits=10, decimal_places=2, default=0, help_text=_(
        'The total amount to be charged to the customer.'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self) -> str:
        return self.product.name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.DO_NOTHING, related_name='order_items')
    sku = models.CharField(_('sku'), max_length=255, blank=True)
    quantity = models.IntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self) -> str:
        return self.product.name


class OrderPayment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.DO_NOTHING, related_name='payments')
    payment_method = models.IntegerField(
        _('payment method'), choices=cart_constants.PAYMENT_METHOD_CHOICES, default=cart_constants.CREDIT_CARD)
    transaction_id = models.CharField(
        _('transaction id'), max_length=255, blank=True)
    amount = models.DecimalField(
        _('amount'), max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(
        _('status'), choices=cart_constants.PAYMENT_STATUS_CHOICES, default=cart_constants.PENDING)
    raw_response = models.TextField(_('raw response'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self) -> int:
        return self.order.id


class OrderShipment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.DO_NOTHING, related_name='shipments')
    tracking_number = models.CharField(
        _('tracking number'), max_length=255, blank=True)
    shipping_method = models.CharField(
        _('shipping method'), max_length=255, blank=True)
    status = models.IntegerField(
        _('status'), choices=cart_constants.SHIPMENT_STATUS_CHOICES, default=cart_constants.PENDING)
    shipped_at = models.DateTimeField(_('shipped at'), null=True, blank=True)
    delivered_at = models.DateTimeField(
        _('delivered at'), null=True, blank=True)
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self) -> int:
        return self.order.id


class OrderReturn(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='orders_return')
    raw_response = models.TextField(_('raw response'), blank=True)

    def __str__(self) -> int:
        return self.order.id
