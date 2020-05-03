from django import forms
from rest_framework import serializers
from account.models import User, Profile
from account.utils import send_register_confirm_email


class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'head_img', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    accepted_number = serializers.ReadOnlyField()
    submission_number = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # profile = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True)
    # TODO profile超链接bug待修复
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class RegisterForm(forms.ModelForm):
    captcha = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'captcha']


class ResetPasswordForm(forms.Form):
    captcha = forms.CharField(required=True)
    email = forms.EmailField(required=True)
