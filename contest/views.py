from rest_framework import viewsets, permissions
from contest.models import Contest, ContestParticipant
from contest.serializers import ContestSerializer, ContestAdminSerializer, ContestListSerializer
from django.shortcuts import get_object_or_404
from account.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core import exceptions


class ContestAdminAPI(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContestAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Contest.objects.filter(visible=True)
    serializer_class = ContestSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return ContestListSerializer
    #     else:
    #         return ContestSerializer


def participate(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)

    try:
        ContestParticipant.objects.filter(participant_id=user.id).get(participate_to_id=contest.id)

    except exceptions.ObjectDoesNotExist:
        contest.participants.add(user)
        return HttpResponseRedirect('../')

    else:
        messages.MessageFailure('Failed')
        return HttpResponse('您已经参加此比赛，请不要重复参与')
