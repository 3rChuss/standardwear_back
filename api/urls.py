# Register your views url here (general)
from django.urls import path, include
from users import urls as users_urls
from products import urls as products_urls

api_version = 'v1/'

urlpatterns = [
    path('users/', include(users_urls)),
    path('auth/register', users_urls.UserRegisterView.as_view(), name='register'),
    path('auth/login', users_urls.UserLoginView.as_view(), name='login'),
    path('products/', include(products_urls)),
]


# Add api version to urls
urlpatterns = [
    path(api_version, include(urlpatterns)),
]
