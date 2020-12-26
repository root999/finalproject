from django.db import models
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

    
class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE,primary_key=True,related_name='menu')
    products= models.ManyToManyField(to=Product,blank=True)

class Customer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)


class Order(models.Model):
    orderedProducts = models.ManyToManyField(to=Product,blank=True)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,related_name='order')
    restaurant = models.OneToOneField(Restaurant,on_delete=models.CASCADE,related_name='order')
    issueTime = models.DateTimeField(auto_now_add=True)
    

