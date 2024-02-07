from rest_framework import serializers


class DataFrameSerializer(serializers.Serializer):
    data = serializers.JSONField()
