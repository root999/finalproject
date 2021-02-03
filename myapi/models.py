from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from datetime import  date
import datetime

class Customer(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(blank=True, max_length=100)
    surname = models.CharField(blank=True, max_length=100,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname']

    objects = CustomUserManager()

  

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    photoUrl = models.URLField(blank=True)
    category = models.CharField(max_length=50)
    details = models.CharField(max_length=250)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    logoUrl = models.URLField(blank=True)
    max_work = models.IntegerField(default=5)
    active_work = models.IntegerField(default=0)
    begin_time =models.TimeField(default= datetime.time(8,00,00))
    end_time = models.TimeField(default=datetime.time(23,00,00))

    
class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE,primary_key=True,related_name='menu')
    products= models.ManyToManyField(to=Product,blank=True)

# class Customer(models.Model):
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)


class Order(models.Model):
    orderedProducts = models.ManyToManyField(to=Product,blank=True,through="ProductsInOrder")
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='order')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='order')
    issueDate = models.DateField(auto_now_add=True)
    issueTime = models.TimeField(auto_now_add=True)
    plannedDate = models.DateField(default=date.today)
    plannedTime = models.TimeField(default=datetime.time)
    status = models.CharField(max_length=10,default="Active")
    detail = models.CharField(max_length=100,default="")
   
  
class ProductsInOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    productCount = models.IntegerField(default=0)


class RestaurantOwner(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE,primary_key=True,related_name='owner')




