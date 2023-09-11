from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from translations.models import Language
from .models import Product
from .serializers import (
    ProductTranslationSerializer,
)

# Create your views here.

class ProductListView(APIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['reference', 'product_variant__description', 'category__name', 'product_variant_reference']
    serializer_class = ProductTranslationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ['referece', 'product_variant__description', 'category__name', 'product_variant_reference']
    ordering_fields = ['reference', 'product_variant__description', 'category__name', 'product_variant_reference']

    def get_queryset(self):
        # get request get content-language
        language = Language.objects.get(code=self.request.headers.get('Accept-Language'))

        # filter queryset by language
        return Product.objects.filter(translations__language=language)


    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)



class ProductDetailView(APIView):
    serializer_class = ProductTranslationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # get request get content-language
        language = Language.objects.get(code=self.request.headers.get('Accept-Language'))

        # filter queryset by language
        return Product.objects.filter(translations__language=language)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, context={'request': request})
        return Response(serializer.data)
    

class ProductCreateView(APIView):
    serializer_class = ProductTranslationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
