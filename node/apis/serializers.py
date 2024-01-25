from rest_framework import serializers
from .. import models


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Node
        fields = '__all__'


class NodeConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NodeConnection
        fields = '__all__'