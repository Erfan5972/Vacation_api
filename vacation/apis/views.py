from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import VacationSerializer, VacationResponseSerializer
from .. models import Vacation, VacationResponse
from ..permissions import CanCreateVacationResponse


class VacationViewSet(viewsets.ModelViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    # permission_classes = [IsAuthenticated]


class VacationResponseViewSet(viewsets.ModelViewSet):
    queryset = VacationResponse.objects.all()
    serializer_class = VacationResponseSerializer
    permission_classes = [IsAuthenticated, CanCreateVacationResponse]
