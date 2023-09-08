from django.urls import path
from .views import ListUsersView, UserDetailView, UserMeView, UserAddressView, UserRegisterView, UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('', ListUsersView.as_view(), name="users-all"),
    path('<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('me/', UserMeView.as_view(), name="user-me"),
    path('address/', UserAddressView.as_view(), name="user-address"),
    path('address/<int:pk>/', UserAddressView.as_view(),
         name="user-address-detail"),
]
