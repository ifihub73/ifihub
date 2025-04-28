from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('<int:pk>/', views.view_profile, name='view_profile'),
    path('edit-profile-home/<int:pk>', views.edit_profile_home, name='edit_profile_home'),
]