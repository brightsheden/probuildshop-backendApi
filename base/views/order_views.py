

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
#from .products import products
from rest_framework.response import Response
from base.models import Product, Order,OrderItem,ShippingAddress
from base.serializer import *
from rest_framework import  serializers, status
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems (request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        message = {'deatail': 'No order item'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice= data['shippingPrice'],
            totalPrice = data['totalPrice']
        )
        # 2 create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],

        )
        # 3  create orderItems and set order to orderItem relationship

        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            #product = Product.objects.get(_id=1['product'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price=i['price'],
                image = product.image.url
            )

        # 4 update stock
            product.countInstock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)

        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({"detail":"Not authorised to view this order"},
            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail":"order doese not exist"}, status=status.HTTP_400_BAD_REQUEST)
        