from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import filters
from .models import *
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from collections import defaultdict

from surprise import Dataset,Reader
from surprise import SVD
from surprise.model_selection import KFold
import pandas as pd
from surprise import accuracy
from django.http import JsonResponse

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return PostOrderSerializer
        return OrderSerializer 
    serializer_class = OrderSerializer
   
    queryset = Order.objects.all()



def get_top_n_for_user(user_id,predictions, n=10):
    print(user_id)
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, str(est)))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n[user_id]



@api_view()
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def recommendation(request):
    print(request.user.id)
    df = pd.read_csv("R:/mixedcodes/restapi/finalproject2/myapi/NanChangeTo0.csv")
    reader = Reader()
    data = Dataset.load_from_df(df,reader)
    algo = SVD()
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    testset=trainset.build_testset()
    predictions = algo.test(testset)
    for_user = get_top_n_for_user(request.user.id,predictions,n=20)
  
    res = {'recommendation':for_user}
    return Response(res)
   
   
    