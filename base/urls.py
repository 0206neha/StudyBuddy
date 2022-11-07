#this is apps uri file we create this file for mapping of urls in our app when we request the django server
from django.urls import path

from . import views

urlpatterns=[

    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    
    path('',views.home,name="home"),    # for home page empty string,views for home,give name for home page
    path('room/<str:pk>/',views.room,name="room"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),
    path('profile/',views.userProfile,name="user-profile"),




]