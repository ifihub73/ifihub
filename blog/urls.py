from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='blog_home'),
    path('check-auth/', views.check_authenticated, name='check_auth'),
    path('create-blog-home/', views.create_blog_home, name='create_blog_home'),
    path('upload/', views.upload_image, name='image_upload'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('view-all/', views.view_all, name='view_all'),
    path('one-blog/<int:pk>', views.view_one, name='view_one'),
    path('like-blog/<int:pk>/', views.like_post, name='like_blog'),
    path('make-comment/<int:pk>/', views.make_comment, name='make_comments'),
]