from django.urls import path

from user.apis import views

app_name = 'user'
urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='user-register'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('logout/', views.UserLogout.as_view(), name='user-logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh-token'),

]