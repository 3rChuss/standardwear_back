# users/constants.py

SUPERUSER = 'superuser'
ADMIN = 'admin'
COMMERCIANT = 'commerciant'
CLIENT = 'client'

USER_TYPE_CHOICES = (
    (SUPERUSER, 'Superuser'),
    (ADMIN, 'Admin'),
    (COMMERCIANT, 'Commerciant'),
    (CLIENT, 'Client'),
)

SPANISH = 'es'
ENGLISH = 'en'

LANGUAGE_CHOICES = (
    (SPANISH, 'Spanish'),
    (ENGLISH, 'English'),
)


BILLING_ADDRESS = 1
SHIPPING_ADDRESS = 2

ADDRESS_TYPE_CHOICES = (
    (BILLING_ADDRESS, 'Billing Address'),
    (SHIPPING_ADDRESS, 'Shipping Address'),
)
