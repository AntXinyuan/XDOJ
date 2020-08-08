from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account import views

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileAPI.as_view(), name='admin_profile-detail'),
    # path('send_email', views.SendEmailView.as_view()),
    path('', include(router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
