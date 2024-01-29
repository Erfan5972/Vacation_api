from django.urls import path
from . import views


app_name = 'vacation'
urlpatterns = [
    path('', views.VacationCreateView.as_view(), name='create'),
    path('list/', views.VacationListView.as_view(), name='list'),
    path('<int:pk>/', views.VacationRetrieveView.as_view(), name='update-destroy-retrieve'),
    path('response/', views.VacationResponseCreateView.as_view(), name='response-create'),
    path('response/list/', views.VacationResponseListView.as_view(), name='response-list'),
    path('response/<int:pk>/', views.VacationResponseRetrieveView.as_view(), name='response-update-destroy-retrieve'),

]