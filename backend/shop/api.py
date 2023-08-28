from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductsSerializer, UserSerializer, GroupSerializer
from .models import Product, Category
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, generics, authentication
from .models import *
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductsViewSet(viewsets.ModelViewSet): # viewsets.ReadOnlyModelViewSet - Can just read db
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Product.objects.all()
    lookup_field = 'slug'
    # print(queryset.values())

    def get_queryset(self):
        return self.queryset.all()
        # return self.queryset.filter(tag=None)

    def retrieve(self, request, slug=None): # retrieve - GET
        item = get_object_or_404(self.queryset, slug=slug)
        serializer = ProductsSerializer(item)
        return Response(serializer.data)
    # When try to get a one product by slug, image url not contain domain name
    # django rest framework retrieve get full path from db
    # https://github.com/respondcreate/django-versatileimagefield/issues/11
    # TODO Make sure that it works with nginx



    



