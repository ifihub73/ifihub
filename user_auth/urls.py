from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.create_user, name='register'),
    path('login/', views.login_user, name='user_login'),
    path('logout/', views.logout_user, name='logout_user'),
]