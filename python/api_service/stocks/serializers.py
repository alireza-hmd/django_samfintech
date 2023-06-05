from rest_framework import serializers


class StockSerializer(serializers.Serializer):
    user = serializers.CharField()
    stockname = serializers.CharField()
    quantity = serializers.IntegerField()


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
