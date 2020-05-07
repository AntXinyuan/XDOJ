from django import forms
from rest_framework import serializers
from submission.models import Submission, JudgeStatus


class SubmissionListSerializer(serializers.HyperlinkedModelSerializer):
    problem = serializers.SlugRelatedField(slug_field='id', read_only=True)
    author_name = serializers.ReadOnlyField(source='user.username')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return JudgeStatus.dict().get(obj.status)

    class Meta:
        model = Submission
        fields = ['id', 'url', 'create_time', 'author_name', 'problem',
                  'status', 'language', 'statistic_info', 'is_shared']


class SubmissionDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return JudgeStatus.dict().get(obj.status)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'language', 'solution', 'status', 'error_info', 'statistic_info']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Submission
        exclude = ['status', 'statistic_info', 'error_info']


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['is_shared']
