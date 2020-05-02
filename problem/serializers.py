from django import forms
from rest_framework import serializers
from problem.models import Problem, ProblemTag


class ProblemAdminSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    tags = serializers.SlugRelatedField(slug_field='name', many=True, queryset=ProblemTag.objects.all(),
                                        allow_null=True)

    class Meta:
        model = Problem
        fields = '__all__'

    def validate_empty_values(self, data):
        tags = dict(data).get('tags', [])
        for tag_name in tags:
            try:
                tag = ProblemTag.objects.get(name=tag_name)
            except ProblemTag.DoesNotExist:
                tag = ProblemTag.objects.create(name=tag_name)
        return super().validate_empty_values(data)


class ProblemListSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    total = serializers.ReadOnlyField(source='submission_number')
    ac_rate = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ['url', 'id', 'title', 'difficulty', 'tags', 'total', 'ac_rate']

    def get_ac_rate(self, obj):
        if obj.accepted_number:
            return obj.submission_number / obj.accepted_number
        else:
            return 0.00


class ProblemDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Problem
        exclude = ['is_public', 'visible', 'create_time', 'last_update_time', 'created_by', 'test_case_scores', ]

# =============================================================================


class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = ['id', 'name']


class ProblemTagDetailSerializer(serializers.ModelSerializer):
    problems = ProblemListSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemTag
        fields = ['name', 'problems']


class TestCaseUploadForm(forms.Form):
    file = forms.FileField()
