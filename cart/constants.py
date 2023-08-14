from django.utils.translation import gettext_lazy as _

NEW = 1
CART = 2
SAVED = 3
CHECKOUT = 4
ORDERED = 5
PAID = 6
CANCELLED = 7
REFUNDED = 8
SHIPPED = 9
DELIVERED = 10
ABANDONED = 11

CART_STATUS_CHOICES = (
    (NEW, _('New')),
    (CART, _('Cart')),
    (SAVED, _('Saved')),
    (CHECKOUT, _('Checkout')),
    (ORDERED, _('Ordered')),
    (PAID, _('Paid')),
    (CANCELLED, _('Cancelled')),
    (REFUNDED, _('Refunded')),
    (SHIPPED, _('Shipped')),
    (DELIVERED, _('Delivered')),
    (ABANDONED, _('Abandoned')),
)

ONHOLD = 1
PROCESSING = 2
DELIVIRING = 3
DELIVERED = 4
RETURNED = 5

SHIPMENT_STATUS_CHOICES = (
    (ONHOLD, _('On Hold')),
    (PROCESSING, _('Processing')),
    (DELIVIRING, _('Delivering')),
    (DELIVERED, _('Delivered')),
    (CANCELLED, _('Cancelled')),
    (RETURNED, _('Returned')),
)


FAILED = 1
PENDING = 2
DECLINED = 3
REJECTED = 4
SUCCESS = 5

PAYMENT_STATUS_CHOICES = (
    (NEW, _('New')),
    (CANCELLED, _('Cancelled')),
    (FAILED, _('Failed')),
    (PENDING, _('Pending')),
    (DECLINED, _('Declined')),
    (REJECTED, _('Rejected')),
    (SUCCESS, _('Success')),
)


CREDIT_CARD = 1
BANK_TRANSFER = 2
CASH_ON_DELIVERY = 3
BITCOIN = 4


PAYMENT_METHOD_CHOICES = (
    (CREDIT_CARD, _('Credit Card')),
    (BANK_TRANSFER, _('Bank Transfer')),
    (CASH_ON_DELIVERY, _('Cash on Delivery')),
    (BITCOIN, _('Bitcoin')),
)
