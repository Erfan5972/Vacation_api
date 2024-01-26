from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacation', views.VacationViewSet)

urlpatterns = [
    path('', include(router.urls))
]