from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account import views


urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('confirm/', views.RegisterConfirmAPI.as_view()),
    path('change_password/', views.ChangePasswordAPI.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
