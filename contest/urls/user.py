from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from contest import views

router = DefaultRouter()
router.register('', views.ContestAPI)

app_name = 'contest'

urlpatterns = [
    path('<int:contest_id>/participate/', views.participate, name='participate'),
    path('', include(router.urls)),
]
