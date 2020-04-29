from rest_framework import serializers

from announcement.models import Announcement


class CreateAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'visible']


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Announcement
        fields = "__all__"


class EditAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'visible']