
from rest_framework import serializers

from XDOJ import utils, settings
from account.models import User


class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'head_img', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        send_confirm_email(to_user=user, code=user.make_confirm_string())
        return user


def send_confirm_email(to_user, code):

    from django.core.mail import EmailMultiAlternatives

    subject = 'XDOJ注册确认邮件'

    text_content =  '''尊敬的{},您好！ 感谢注册www.xdoj.com，XDOJ是一款致力于编程练习的OJ系统！\n
                    （如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！） \n 
                    你可以手动复制下面的激活链接到浏览器地址栏中访问以完成账户激活！ \n
                    http://{}/account/confirm/?code={} \n
                    此链接有效期为{}天！
                    '''.format(to_user.username, '127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    html_content = '''
                    <p>尊敬的{},您好！</p> \
                    <p>感谢注册<a href="http://{}/account/confirm/?code={}" target=blank>www.XDOJ.com</a>，\
                    XDOJ是一款致力于编程练习的OJ系统！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(to_user.username, '127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

