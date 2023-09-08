from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

import json

from django.contrib.auth.models import User
from django.db import transaction

from .models import UserAddress
from .serializers import UserSerializer, UserAddressSerializer, RegisterSerializer

# Create your views here.


"""
REGISTER
"""


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        """
        Register a user \n
        Create a user instance.
        """
        # check if body
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if request.auth is None:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                        user.set_password(serializer.validated_data['password'])
                        user.save()
                        return Response(
                            status=status.HTTP_201_CREATED)
                        
                except Exception as e:
                    return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_403_FORBIDDEN)


class ListUsersView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]

    def get(self, request, format=None):
        """
        List all users \n
        Return a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a user \n
        Create a user instance.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # bulk delete
    def delete(self, request, format=None):
        """
        Delete users \n
        Delete a list of users.
        """
        ids = request.data.get('ids', None)
        if ids is not None:
            User.objects.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    View to retrieve a user instance.

    * Requires token authentication.
    * Only admin users are able to access this view.
    * Only admin users are write to access this view.
    """
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        """
        Retrieve a user instance \n
        Return a user instance.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update a user instance \n
        Return a user instance.
        """

        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    """
    View to retrieve a user instance.

    * Requires token authentication.
    * Only admin users are able to access this view.
    * Only admin users are able to write this view.
    """
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, format=None):
        """
        Retrieve a user instance \n
        Return a user instance.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        """
        Update a user instance \n
        Return a user instance.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete a user instance \n
        Return a user instance.
        """
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, format=None):
        """
        Activate/Deactivate a user instance \n
        Return a user instance.
        """
        user = request.user
        user.is_active = not user.is_active
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserAddressView(APIView):
    """
    View to retrieve a user address instance.

    * Requires token authentication.
    * Only admin users are able to access this view.
    * Only admin users are able to write this view.
    """
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_object(self, pk):
        try:
            return UserAddress.objects.get(pk=pk)
        except UserAddress.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        """
        Retrieve a user address instance \n
        Return a user address instance.
        """
        user = request.user
        address = UserAddress.objects.filter(user=user)
        serializer = UserAddressSerializer(address, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update a user address instance \n
        Return a user address instance.
        """
        address = self.get_object(pk)
        serializer = UserAddressSerializer(
            address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete a user address instance \n
        Return a user address instance.
        """
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
