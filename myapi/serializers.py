from rest_framework import serializers

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers,fields

from .models import *

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from django.utils.dateparse import parse_date

class ProductSerializer(serializers.ModelSerializer):

    class Meta :
        ordering = ['name']
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
        fields = ("name","id")



class LogCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'email', 'name','surname']
        
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name':user.name,
            'surname':user.surname
        })
class RegisterCustomerSerializer(serializers.Serializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = [ 'email', 'name','surname',
        'password', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }

    def save(self,request):
        user = Customer(
            email=request.data['email'],
            name=request.data['name'],
            surname=request.data['surname']
        )


        password = request.data['password']
        password2 = request.data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['name']
        model = Customer
        fields = ("id","name","surname")

class PostCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['id']
        model = Customer
        fields = ("id","name")
        
class ProductsInOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta :
        ordering = ['-id']
        model = ProductsInOrder
        fields = ('product','productCount')

class OrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(source="productsinorder_set",many=True)
    restaurant = RestaurantSerializer()
    customer = CustomerSerializer()
         
    class Meta:
        ordering = ['-id']
        model = Order
        fields= ("id","products","restaurant","customer","issueDate","issueTime")

class PostOrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(source="productsinorder_set",many=True)
    restaurant = PostRestaurantSerializer()
    customer = CustomerSerializer()
    def create(self,validated_data):
        print(validated_data)
        restaurant_data = validated_data.get('restaurant')
        rest =get_object_or_404(Restaurant,name=restaurant_data['name'])
        customer_data = validated_data.get('customer')
        cust = get_object_or_404(Customer,name=customer_data['name'])
        order = Order.objects.create(customer=cust,restaurant=rest)
       
        order.plannedTime = validated_data.get('plannedTime')
        order.plannedDate = validated_data.get('plannedDate')
        products_data = validated_data.get('productsinorder_set')
        for product in products_data:
           prod = get_object_or_404(Product,name=product['product']['name'])
           ProductsInOrder.objects.create(product=prod,order=order,productCount=product['productCount'])
        order.save()
        return order
    class Meta:
        ordering = ['-id']
        model = Order
        fields= ("id","products","restaurant","customer","plannedTime","plannedDate")

class RecommendationSerializer(serializers.Serializer):
    recommendation = serializers.SerializerMethodField()

  
