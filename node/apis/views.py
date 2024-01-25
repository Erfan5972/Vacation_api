from rest_framework import viewsets
from . import serializers
from .. import models


class NodeViewSet(viewsets.ModelViewSet):
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeSerializer


class NodeConnectionViewSet(viewsets.ModelViewSet):
    queryset = models.NodeConnection.objects.all()
    serializer_class = serializers.NodeConnectionSerializer