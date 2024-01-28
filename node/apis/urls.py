from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('node', views.NodeViewSet)
router.register('node-connection', views.NodeConnectionViewSet)

app_name = 'node'
urlpatterns = [
    path('', include(router.urls))
]