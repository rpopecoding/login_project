from django.urls import path

from . import views

urlpatterns =[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('wall', views.wall),
    path('post_tweet', views.post_tweet),
    path('comment', views.comment),
    path('delete_tweet', views.delete_tweet)

    

]