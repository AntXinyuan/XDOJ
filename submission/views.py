from rest_framework import generics, viewsets, mixins, permissions
from rest_framework.response import Response
from submission.models import Submission, JudgeStatus
from submission.serializers import SubmissionListSerializer, SubmissionDetailSerializer, SubmissionCreateSerializer, \
    SubmissionUpdateSerializer
from utils.tools import str2bool


def judge(submission):
    pass


class SubmissionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_really_authenticated = request and request.user.is_authenticated
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return is_really_authenticated
        elif view.action == 'partial_update':
            return is_really_authenticated and obj.user == request.user
        elif view.action == 'retrieve':
            return obj.is_really_shared() or \
                   is_really_authenticated and obj.user == request.user


class SubmissionAPI(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    queryset = Submission.objects.all()
    permission_classes = [SubmissionPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return SubmissionListSerializer
        elif self.action == 'retrieve':
            return SubmissionDetailSerializer
        elif self.action == 'create':
            return SubmissionCreateSerializer
        elif self.action == 'partial_update':
            return SubmissionUpdateSerializer

    def perform_create(self, serializer):
        submission = serializer.save(user=self.request.user)
        # TODO 待完成：调用评测函数
        # judge(submission.id)

    def list(self, request, *args, **kwargs):
        submissions = Submission.objects.all()
        only_mine = request.GET.get('problem')
        problem_id = request.GET.get('problem')
        language = request.GET.get('language')
        only_ac = request.GET.get('only_ac')
        if str2bool(only_mine) and request.user and request.user.is_authenticated:
            submissions = submissions.filter(user=request.user)
        if problem_id:
            submissions = submissions.filter(problem_id=problem_id)
        if language:
            submissions = submissions.filter(language=language)
        if str2bool(only_ac):
            submissions = submissions.filter(status=JudgeStatus.ACCEPTED)

        page = self.paginate_queryset(submissions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)










