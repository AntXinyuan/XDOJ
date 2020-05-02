from django.urls import path, include
from rest_framework.routers import DefaultRouter

from problem import views

router = DefaultRouter()
router.register('tag', views.ProblemTagAdminAPI)
router.register('', views.ProblemAdminAPI)

urlpatterns = [
    path('test_case/', views.TestCaseAdminAPI.as_view()),
    path('', include(router.urls)),
]