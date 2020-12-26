from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from myapi.views import *
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()



router.register(r'api/products',ProductViewSet,basename='product')
router.register(r'api/restaurants',RestaurantViewSet,basename='restaurant')
router.register(r'api/menus',MenuViewSet,basename='menu')
router.register(r'api/customers',CustomerViewSet,basename='customer')
router.register(r'api/orders',OrderViewSet,basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'',include(router.urls)),
    path(r'api/',include('rest_framework.urls',namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth')
]
