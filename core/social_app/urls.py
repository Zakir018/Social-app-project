from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('photos/', views.photos, name='photos'),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("edit_personal_information/", views.edit_personal_information, name="edit_personal_information"),
    path("change_user_password/",views.change_user_password, name="change_user_password"),
    path('profile/', views.edit_profile, name='profile'),
    path('other_profile/<int:pk>/', views.other_profile, name='other_profile'),
    path('logout/', views.user_logout, name='user_logout'),
    path('setting/', views.setting, name='setting'),
    path('posts/', views.add_post, name='add_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('post_like/<int:pk>/', views.post_like, name="post_like"),
    path('add_comments/', views.add_comments, name='add_comments'),
    path('fetch-comments/<int:pk>/', views.fetch_comments, name="fetch_comments"),
    path('delete_post/<int:pk>/<str:page>/', views.delete_post, name='delete_post'),
    path('group/<int:pk>/', views.group, name='group'),
    path('create_group/', views.create_group, name='create_group'),
    path('about/', views.about, name='about'),
    path('friends/', views.friends, name='friends'),

]

