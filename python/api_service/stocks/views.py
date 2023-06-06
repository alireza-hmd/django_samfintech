from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from . import serializers

import json
import redis

REDIS_CONTAINER = 'redis-redis-1'
r = redis.Redis(host=REDIS_CONTAINER, port=6379, db=0)


class StockView(APIView):
    @extend_schema(request=serializers.StockSerializer, responses=serializers.MessageSerializer)
    def post(self, request):
        serializer = serializers.StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if r.get(data['user']):
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
            message = {'message': 'User Not Found'}
        return Response(serializers.MessageSerializer(instance=message).data)

