from django.urls import path
from .views import ListUsersView, UserDetailView, UserMeView, UserAddressView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('', ListUsersView.as_view(), name="users-all"),
    path('<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('me/', UserMeView.as_view(), name="user-me"),
    path('address/', UserAddressView.as_view(), name="user-address"),
    path('address/<int:pk>/', UserAddressView.as_view(),
         name="user-address-detail"),
]
