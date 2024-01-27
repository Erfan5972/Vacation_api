from rest_framework import viewsets
from . import serializers
from .. import models
from ..permissions import IsAdminOrReadOnly


class NodeViewSet(viewsets.ModelViewSet):
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeSerializer
    permission_classes = [IsAdminOrReadOnly]


class NodeConnectionViewSet(viewsets.ModelViewSet):
    queryset = models.NodeConnection.objects.all()
    serializer_class = serializers.NodeConnectionSerializer
    permission_classes = [IsAdminOrReadOnly]