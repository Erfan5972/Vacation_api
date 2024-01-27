from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacation', views.VacationViewSet)
router.register('vacation-response', views.VacationResponseViewSet)

urlpatterns = [
    path('', include(router.urls))
]