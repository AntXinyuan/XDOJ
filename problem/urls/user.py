from django.urls import path, include
from rest_framework.routers import DefaultRouter

from problem import views

router = DefaultRouter()
router.register('', views.ProblemAPI)

urlpatterns = [
    path('', include(router.urls)),
]