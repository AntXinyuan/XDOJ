from django.urls import path, include
from rest_framework.routers import DefaultRouter
from submission import views

router = DefaultRouter()
router.register('', views.SubmissionAPI)

urlpatterns = [
    path('', include(router.urls)),
]