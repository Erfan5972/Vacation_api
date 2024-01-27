from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .. import models
from ..permissions import IsAdminOrReadOnly


class NodeViewSet(viewsets.ModelViewSet):
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]


class NodeConnectionViewSet(viewsets.ModelViewSet):
    queryset = models.NodeConnection.objects.all()
    serializer_class = serializers.NodeConnectionSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]