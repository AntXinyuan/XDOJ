from django.urls import path, include
from announcement import views

urlpatterns = [
    path('', views.AnnouncementAPI.as_view()),
]