
from rest_framework import serializers

from XDOJ import utils, settings
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
    #profile = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True)
    # TODO profile超链接bug待修复
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        send_register_confirm_email(to_user=user, confirm_code=user.make_confirm_string())
        return user

