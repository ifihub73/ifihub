from django.urls import path
from . import views

urlpatterns =[
    path('', views.verify_home, name='verify_index'),
    path('save-profile/', views.save_profile, name='save'),
    path('request-question', views.send_question, name='send_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('editor-request-home', views.editor_request_home, name='editor_home'),
    path('submit-request/', views.submit_request, name='submit_request'),
]