# products/constants.py
from django.utils.translation import gettext_lazy as _

NEW = 1
FEATURED = 2
BESTSELLER = 3
SALE = 4
NEW_ARRIVALS = 5

PRODUCT_STATUS_CHOICES = (
    (NEW, _('New')),
    (FEATURED, _('Featured')),
    (BESTSELLER, _('Bestseller')),
    (SALE, _('Sale')),
    (NEW_ARRIVALS, _('New Arrivals')),
)
