from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import VacationCreateSerializer, VacationResponseCreateSerializer, \
    VacationListSerializer, VacationUpdateSerializer, VacationResponseListSerializer

from .. models import Vacation, VacationResponse
from ..permissions import CanCreateVacationResponse


class VacationCreateView(generics.CreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationCreateSerializer
    permission_classes = [IsAuthenticated]


class VacationListView(generics.ListAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationListSerializer
    permission_classes = [IsAuthenticated]


class VacationRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationUpdateSerializer
    permission_classes = [IsAuthenticated]


class VacationResponseCreateView(generics.CreateAPIView):
    queryset = VacationResponse.objects.all()
    serializer_class = VacationResponseCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateVacationResponse]


class VacationResponseListView(generics.ListAPIView):
    queryset = VacationResponse.objects.all()
    serializer_class = VacationResponseListSerializer
    permission_classes = [IsAuthenticated]


class VacationResponseRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VacationResponse.objects.all()
    serializer_class = VacationResponseListSerializer
    permission_classes = [IsAuthenticated]