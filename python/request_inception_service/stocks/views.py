import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.urls import reverse
from . import serializers
import threading
import time
import random
import json
import redis

REDIS_CONTAINER = 'redis-redis-1'
r = redis.Redis(host=REDIS_CONTAINER, port=6379, db=0)


def verify_user(user_id):
    time.sleep(random.randint(1, 100))
    return 0


def verification(url, data):
    response = requests.post(url, data=data)


class VerifyUser(APIView):
    @extend_schema(request=serializers.StockSerializer, responses=serializers.MessageSerializer)
    def post(self, request):
        serializer = serializers.StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        start = time.time()
        verify_user(data['user'])
        end = time.time()
        if (end - start) <= 60:
            if r.get(data['stockname']):
                stock = json.loads(r.get(data['stockname']))
                n = -1
                while not stock['price'][n]:
                    n -= 1
                stock_price = int(stock['price'][n])
                user = json.loads(r.get(data['user']))
                if user['credit'] >= stock_price * data['quantity']:
                    message = {'message': 'Accept'}
                else:
                    message = {'message': 'Deny'}
            else:
                message = {'message': 'Invalid Stock Name'}
        else:
            message = {'message': 'Server is not responding. try again later'}
        return Response(serializers.MessageSerializer(instance=message).data)


class StockView(APIView):
    @extend_schema(request=serializers.StockSerializer, responses=serializers.MessageSerializer)
    def post(self, request):
        serializer = serializers.StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if r.get(data['user']):
            url = request.build_absolute_uri(reverse('verify_user'))
            t = threading.Thread(target=verification, args=[url, data]).start()
            message = {'message': 'Working on your request'}
        else:
            message = {'message': 'User not Found'}
        return Response(serializers.MessageSerializer(instance=message).data)
