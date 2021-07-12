
from django.urls import path
from base.views import  order_views as views
#from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('add/', views.addOrderItems, name='orders-add'),
    path('<str:pk>/', views.getOrderById, name='user-order')
]