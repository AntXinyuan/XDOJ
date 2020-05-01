import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from XDOJ.utils import get_dict, SuccessResponse, ErrorResponse
from account.models import User, ConfirmString, Profile
from account.serializers import UserAdminSerializer, UserSerializer, RegisterSerializer, ProfileSerializer
from XDOJ import utils
from account.utils import send_reset_password_email


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsUserselfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS) or obj.user == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserselfOrReadOnly]


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginAPI(generics.GenericAPIView):
    def put(self, request):
        # if request.user.is_authenticated:
        #    return JsonResponse(utils.response_dict(message='你已经登陆过了！', data=UserSerializer(request.user)))
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_confirmed:
                login(request, user)
                serializer = UserSerializer(user)
                return SuccessResponse(msg=serializer.data)
            else:
                return ErrorResponse(msg='账户尚未激活！')
        else:
            return ErrorResponse(msg='用户名或密码错误！')


class LogoutAPI(generics.GenericAPIView):
    def put(self, request):
        logout(request)
        return SuccessResponse(msg='登出成功！')


class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def put(self, request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return SuccessResponse(msg="密码修改成功！")
        else:
            return ErrorResponse(msg='旧密码错误，请重新输入！')


class ResetPasswordAPI(generics.GenericAPIView):
    def post(self, request):
        if request.user.is_authenticated:
            return ErrorResponse(msg='您已登陆，无需重置密码', http_status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ErrorResponse(msg='邮箱有误，对应用户不存在')

        confirm_code = user.make_confirm_string()
        send_reset_password_email(to_user=user, reset_code=confirm_code)
        return SuccessResponse(msg='重置请求成功，请及时查收邮件！')


class Confirmviewset(viewsets.GenericViewSet):
    @action(methods=['POST'], detail=False)
    def reset_password(self, request):
        code = request.data['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except ConfirmString.DoesNotExist:
            return ErrorResponse(msg='确认码不存在')
        if confirm.is_expired():
            confirm.delete()
            return ErrorResponse(msg='您的邮件已经过期！请重新注册!')
        else:
            new_password = request.data['new_password']
            confirm.user.set_password(new_password)
            confirm.user.save()
            confirm.delete()
            return SuccessResponse(msg='密码重置成功, 请使用新密码登录！')

    @action(methods=['GET'], detail=False)
    def register(self, request):
        code = request.GET['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except ConfirmString.DoesNotExist:
            return ErrorResponse(msg='确认码不存在')
        if confirm.is_expired():
            confirm.user.delete()
            return ErrorResponse(msg='您的邮件已经过期！请重新注册!')
        else:
            confirm.user.is_confirmed = True
            confirm.user.save()
            confirm.delete()
            return SuccessResponse(msg='感谢确认，请使用账户登录！')