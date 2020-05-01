from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account import views

router = DefaultRouter()
router.register('confirm', views.Confirmviewset, basename='confirm')

urlpatterns = [
    path('captcha/', views.CaptchaAPIView.as_view(), name='captcha'),
    path('profile/<int:pk>/', views.ProfileAPI.as_view(), name='profile-detail'),
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('change_password/', views.ChangePasswordAPI.as_view()),
    path('reset_password/', views.ResetPasswordAPI.as_view()),
    path('', include(router.urls))
]

#urlpatterns = format_suffix_patterns(urlpatterns)
