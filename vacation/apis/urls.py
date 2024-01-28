from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacation', views.VacationViewSet, basename='create-vacation')
router.register('vacation-response', views.VacationResponseViewSet, basename='create-vacation-response')

app_name = 'vacation'
urlpatterns = [
    path('', include(router.urls))
]