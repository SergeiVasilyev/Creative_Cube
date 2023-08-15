from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ShoppingSession, Product, Order, OrderItem, Image


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'img_name')

class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True) # read_only=True - необязательное поле при POST запросе
    images = ImageSerializer(many=True)
    class Meta:
        model = Product # Product - модель из models.py
        fields = ('id', 'name', 'description', 'price', 'images', 'category', 'category_name', 'tag', 'availability', 'date_added', 'quantity', 'slug')
        lookup_field = 'slug' # slug - поле по которому будет искаться товар
        extra_kwargs = {
            'url': {'lookup_field': 'slug'} 
        }


