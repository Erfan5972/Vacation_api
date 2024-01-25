from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('node', views.NodeViewSet)
router.register('node-connection', views.NodeConnectionViewSet)

urlpatterns = [
    path('', include(router.urls))
]