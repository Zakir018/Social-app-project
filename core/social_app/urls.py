from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('photos/', views.photos, name='photos'),
    path('friends/', views.friends, name='friends'),
    path('posts/', views.add_post, name='add_post'),
    path('post/<int:pk>/<str:page>/', views.delete_post, name='delete_post'),

]

