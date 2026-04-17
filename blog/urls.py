from django.urls import path
from .views import *
from .api import post_list_api

app_name = 'blog'

urlpatterns =[
    # path('')
    path('',post_list, name='post_list'),
    path('post/<slug:slug>/',post_detail, name='post_detail'),
    path('post-add/', post_add, name="post_add"),
    path('post/<slug:slug>/delete', post_delete, name='post_delete'),
    path('post/<slug:slug>/edit',post_edit, name="post_edit" ),

    #user
    path('my-posts',user_posts, name='user_posts'),

        # NEW HTMX URLs
    path('post/<slug:slug>/comments/', comment_list, name='comment_list'),
    path('post/<slug:slug>/comment/add/', add_comment_htmx, name='add_comment_htmx'),
    path('comment/<int:comment_id>/reply/', reply_form, name='reply_form'),

    # API
    path('api/posts/', post_list_api, name= 'post_list_api'),
]
