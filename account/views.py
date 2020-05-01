from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from account import perms
from utils.tools import SuccessResponse, ErrorResponse, img2base64
from account.models import User, ConfirmString, Profile
from account.serializers import UserAdminSerializer, UserSerializer, ProfileSerializer, RegisterForm, ResetPasswordForm
from account.utils import send_reset_password_email, send_register_confirm_email
from utils.captcha import Captcha


class CaptchaAPIView(generics.GenericAPIView):
    def get(self, request):
        # TODO DEBUG 发布时应删除err
        return SuccessResponse(msg=img2base64(Captcha(request).get()), err=Captcha(request).get_answer())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [perms.IsAdminUser]


class ProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [perms.IsBOwnerOrReadOnly]


class RegisterAPI(generics.GenericAPIView):
    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            register_captcha = Captcha(request)
            form_captcha = data.pop('captcha')
            if register_captcha.check(form_captcha):
                user = User.objects.create(**data)
                send_register_confirm_email(to_user=user, confirm_code=user.make_confirm_string())
                return SuccessResponse(msg='注册成功，请及时查收激活邮件！')
            else:
                return ErrorResponse(msg='验证码错误！')
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


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
                return SuccessResponse(msg='ok')
            else:
                return ErrorResponse(msg='账户尚未激活！')
        else:
            return ErrorResponse(msg='用户名或密码错误！')


class LogoutAPI(generics.GenericAPIView):
    def put(self, request):
        logout(request)
        return SuccessResponse(msg='登出成功！')


class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes = [perms.IsOneself]

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

        form = ResetPasswordForm(request.data)
        if form.is_valid():
            data = form.cleaned_data
            reset_password_captcha = Captcha(request)
            form_captcha = data['captcha']
            if reset_password_captcha.check(form_captcha):
                try:
                    user = User.objects.get(email=data['email'])
                except User.DoesNotExist:
                    return ErrorResponse(msg='邮箱有误，对应用户不存在')
                if user.has_reset_password_today():
                    return ErrorResponse(msg='一天只能重置一次密码！')
                else:
                    confirm_code = user.make_confirm_string()
                    user.record_reset_password_time()
                    send_reset_password_email(to_user=user, reset_code=confirm_code)
                    return SuccessResponse(msg='重置请求成功，请及时查收邮件！')
            else:
                return ErrorResponse(msg='验证码错误！')
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class Confirmviewset(viewsets.GenericViewSet):
    @action(methods=['GET'], detail=False)
    def reset_password(self, request):
        code = request.GET['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except ConfirmString.DoesNotExist:
            return ErrorResponse(msg='确认码无效！')
        if confirm.is_expired():
            confirm.delete()
            return ErrorResponse(msg='您的邮件已经过期！请重新注册!')
        else:
            # new_password = request.data['new_password']
            new_password = '1234567'
            confirm.user.set_password(new_password)
            confirm.user.save()
            confirm.delete()
            return SuccessResponse(msg='密码重置成功, 请使用初始密码登录， 并尽快登录修改！')

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