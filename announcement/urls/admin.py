from django.urls import path, include
from rest_framework.routers import DefaultRouter

from announcement import views

router = DefaultRouter()
router.register('', views.AnnouncementAdminAPI)

urlpatterns = [
    path('', include(router.urls)),
]