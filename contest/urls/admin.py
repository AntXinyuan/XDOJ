from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contest import views

router = DefaultRouter()
router.register('', views.ContestAdminAPI)

urlpatterns = [
    path('', include(router.urls)),
]