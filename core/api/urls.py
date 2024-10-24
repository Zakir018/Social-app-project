from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.UserLoginView.as_view(),),
    path('user_signup/', views.UserSignupView.as_view()),
]
