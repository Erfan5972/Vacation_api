from rest_framework import viewsets

from .serializers import VacationSerializer, VacationResponseSerializer
from .. models import Vacation, VacationResponse


class VacationViewSet(viewsets.ModelViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer


class VacationResponseViewSet(viewsets.ModelViewSet):
    queryset = VacationResponse.objects.all()
    serializer_class = VacationResponseSerializer

