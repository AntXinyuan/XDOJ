import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from account.models import User, ConfirmString
from account.serializers import UserAdminSerializer, UserSerializer, RegisterSerializer
from XDOJ import utils


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RegisterConfirmAPI(generics.GenericAPIView):
    def get(self, request):
        code = request.data['code']
        confirm = get_object_or_404(queryset=ConfirmString.objects.all(), code=code)
        now = datetime.datetime.now()
        if now > confirm.create_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse(utils.response_dict(detail='您的邮件已经过期！请重新注册!'), status=status.HTTP_404_NOT_FOUND)
        else:
            confirm.user.is_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse(utils.response_dict(detail='感谢确认，请使用账户登录！'))


class LoginAPI(generics.GenericAPIView):
    def put(self, request):
        if request.user.is_authenticated:
            return JsonResponse(utils.response_dict(message='你已经登陆过了！', data=UserSerializer(request.user)))
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_confirmed:
                login(request, user)
                serializer = UserSerializer(user)
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(utils.response_dict(detail='账户尚未激活！'), status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(utils.response_dict(detail='用户名或密码错误！'), status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(generics.GenericAPIView):
    def put(self, request):
        logout(request)
        return Response(data={'details': '登出成功！'})


class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return JsonResponse(utils.response_dict(message="密码修改成功！"))
        else:
            return JsonResponse(utils.response_dict(message='旧密码错误，请重新输入！'))
