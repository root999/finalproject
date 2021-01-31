from allauth.account.views import confirm_email
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
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('accounts-rest/registration/account-confirm-email/<int:pk>/', confirm_email, name='account_confirm_email'),
    path('recommendation/',recommendation)
]
