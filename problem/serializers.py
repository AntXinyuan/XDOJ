from abc import ABC

from rest_framework import serializers
from problem.models import Problem


class ProblemAdminSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Problem
        fields = '__all__'


class ProblemListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = ['url', 'id', 'title']


class ProblemSerializer(serializers.ModelSerializer):
    tag = serializers.Hyperlink
    class Meta:
        model = Problem
        exclude = ['is_public', 'visible', 'create_time', 'last_update_time', 'created_by', 'test_case_scores', ]
