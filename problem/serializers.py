from rest_framework import serializers
from problem.models import Problem, ProblemTag


class ProblemAdminSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    tags = serializers.SlugRelatedField(slug_field='name', many=True, queryset=ProblemTag.objects.all(), allow_null=True)

    class Meta:
        model = Problem
        fields = '__all__'


class ProblemListSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Problem
        fields = ['url', 'id', 'title', 'difficulty', 'tags']


class ProblemDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Problem
        exclude = ['is_public', 'visible', 'create_time', 'last_update_time', 'created_by', 'test_case_scores', ]


class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = ['id', 'name']


class ProblemTagDetailSerializer(serializers.ModelSerializer):
    problems = ProblemListSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemTag
        fields = ['name', 'problems']
