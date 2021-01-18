from rest_framework import serializers

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
    menu = MenuSerializer( read_only =True)
    class Meta:
        ordering = ['-id']
        model = Restaurant
        fields = ("id","name","address","logoUrl","menu")


class PostRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Restaurant
        fields = ("name",)



class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['name']
        model = Customer
        fields = ("id","name","surname")

class PostCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['name']
        model = Customer
        fields = ("name",)
        
class ProductsInOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta :
        ordering = ['-id']
        model = ProductsInOrder
        fields = ('id','product','productCount')

class OrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(source="productsinorder_set",many=True)
    restaurant = RestaurantSerializer()
    customer = CustomerSerializer()
         
    class Meta:
        ordering = ['-id']
        model = Order
        fields= ("id","products","restaurant","customer","issueTime")

class PostOrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(source="productsinorder_set",many=True)
    restaurant = PostRestaurantSerializer()
    customer = PostCustomerSerializer()
    
    def create(self,validated_data):
        #print(validated_data)
        restaurant_data = validated_data.get('restaurant')
        rest =get_object_or_404(Restaurant,name=restaurant_data['name'])
        customer_data = validated_data.get('customer')
        cust = get_object_or_404(Customer,name=customer_data['name'])
        order = Order.objects.create(customer=cust,restaurant=rest)
     
        products_data = validated_data.get('productsinorder_set')
        for product in products_data:
           prod = get_object_or_404(Product,name=product['product']['name'])
           ProductsInOrder.objects.create(product=prod,order=order,productCount=product['productCount'])
        return order




    class Meta:
        ordering = ['-id']
        model = Order
        fields= ("id","products","restaurant","customer","issueTime")


