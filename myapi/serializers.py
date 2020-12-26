from rest_framework import serializers

from django.contrib.auth.models import User

from .models import *





class ProductSerializer(serializers.ModelSerializer):

    class Meta :
        ordering = ['-id']
        model = Product
        fields = ('id','name','price','photoUrl','category','details')
        

class MenuSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        ordering = ['-id']
        model = Menu
        fields = ("restaurant","products")
        extra_kwargs = {'products':{'required':False}}


class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(source="menu", read_only =True)
    class Meta:
        ordering = ['-id']
        model = Restaurant
        fields = ("id","name","address","logoUrl","menus")



class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['name']
        model = Customer
        fields = ("id","name","surname")

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(source="orderedProducts",many=True,read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    class Meta:
        ordering = ['-id']
        model = Order
        fields= ("id","restaurant","customer","products")