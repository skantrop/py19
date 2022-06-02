from .models import Category, Product, Review
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'image')
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = instance.category.title
        representation['reviews'] = instance.reviews.all().count()
        return representation

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ('author', )
    
    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = instance.category.title
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes'] = instance.likes.filter(is_liked=True).count()
        return representation

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('author', )

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.title
        representation['author'] = instance.author.email
        return representation
    
class  FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'