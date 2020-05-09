from rest_framework import serializers
from contest.models import Contest


class ContestAdminSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Contest
        fields = '__all__'


class ContestListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ['url', 'id', 'title']


class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        exclude = ['visible', 'created_by']

