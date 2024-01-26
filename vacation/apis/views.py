from rest_framework import viewsets

from .serializers import VacationSerializer
from .. models import Vacation


class VacationViewSet(viewsets.ModelViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

