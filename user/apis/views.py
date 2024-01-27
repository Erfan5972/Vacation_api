from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from user.apis.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, RefreshTokenSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserLogin(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status.HTTP_302_FOUND)
        return Response(serializer.data, status.HTTP_404_NOT_FOUND)


class UserLogout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"data": serializer.data, "msg": "you logged out successfully"}, status.HTTP_200_OK)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)