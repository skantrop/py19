from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import CategorySerializer
from .models import Product, Likes, Favorite
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
import django_filters.rest_framework as filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAuthororAdminPermission


class CategoryCreateView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['title', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return super().get_serializer_class()
    

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['like', ]:
            return [IsAuthenticated()]
        return []
    
    # products/1/like/
    @action(detail=True, methods=['GET'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = Likes.objects.get_or_create(product=product,user=user)
        if like_obj.is_liked == False:
            like_obj.is_liked = not like_obj.is_liked
            like_obj.save()
            return Response('You liked this product')
        else:
            like_obj.is_liked = not like_obj.is_liked
            like_obj.save()
            return Response('You disliked this product')
    
    # products/1/favorite/
    @action(detail=True, methods=['GET'])
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = Favorite.objects.get_or_create(product=product,user=user)
        if fav.favorite == False:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Added to favs')
        else:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Not in favs')



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return []
        elif self.action == 'create':
            return [IsAuthenticated()]
        # update, partial_update, destroy
        return [IsAuthororAdminPermission()]
    
    # def get_serializer_context(self):
    #     return {'request': self.request}

        
class FavoriteView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # SELECT * from PRODUCT WHERE user = request.user and Product.favorite == True
        #                          rel_name   FK                      rel_name     boolean_field
        queryset = queryset.filter(favorites__user=self.request.user, favorites__favorite=True)
        return queryset