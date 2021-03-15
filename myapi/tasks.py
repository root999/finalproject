from .models import Order,ProductsInOrder,Restaurant
from datetime import  date
import datetime
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum

def update_delivered_orders_status():
    """
    Deletes all orders that are more than a minute old
    """
    today = date.today()
    one_minute_ago = (datetime.datetime.now() - datetime.timedelta(minutes=1)).time()
    expired_orders = Order.objects.filter(
        Q(plannedTime__lte=one_minute_ago) & Q(plannedDate__lte = today) 
    )
    active_orders = expired_orders.exclude(status="Delivered")
    for element in active_orders:
        productCount = ProductsInOrder.objects.filter(order=element).aggregate(Sum('productCount'))
        count = productCount['productCount__sum']
        print(element)
        rests = Restaurant.objects.filter(id=element.restaurant.id)
        rest = rests[0]
        if rest.active_work >= count:
            rest.active_work = rest.active_work - count
        else:
            rest.active_work = 0
        rest.save()
    expired_orders.update(status="Delivered")