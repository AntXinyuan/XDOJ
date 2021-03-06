from rest_framework import generics, viewsets

from account import perms
from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementAdminAPI(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [perms.IsAdminUser]

    def perform_create(self, serializer):
        from account.models import User
        serializer.save(created_by=User.objects.get(username='admin'))#self.request.user)


class AnnouncementAPI(generics.ListAPIView):
    queryset = Announcement.objects.filter(visible=True)
    serializer_class = AnnouncementSerializer
