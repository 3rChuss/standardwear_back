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


# membership
MEMBERSHIP_FREE = 1
MEMBERSHIP_BASIC = 2
MEMBERSHIP_PREMIUM = 3

MEMBERSHIP_TYPE_CHOICES = (
    (MEMBERSHIP_FREE, 'Free'),
    (MEMBERSHIP_BASIC, 'Basic'),
    (MEMBERSHIP_PREMIUM, 'Premium'),
)
