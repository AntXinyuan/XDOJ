from django.urls import path, include
from rest_framework.routers import DefaultRouter

from problem import views

router = DefaultRouter()
router.register('tag', views.ProblemTagAPI)
router.register('', views.ProblemAPI, basename='problem')

urlpatterns = [
    path('', include(router.urls)),
]