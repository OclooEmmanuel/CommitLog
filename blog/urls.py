from django.urls import path
from .views import *

urlpatterns =[
    path('',post_list, name='post_list'),
    path('post/<slug:slug>/',post_detail, name='post_detail'),
    path('post-add/', post_add, name="post_add"),
    path('post/<slug:slug>/delete', post_delete, name='post_delete'),
    path('post/<slug:slug>/edit',post_edit, name="post_edit" ),

    #user
    path('my-posts',user_posts, name='user_posts')
]
