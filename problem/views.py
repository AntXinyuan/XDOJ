import random

from django.shortcuts import redirect
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from XDOJ import utils
from problem.models import Problem, ProblemTag
from problem.serializers import ProblemAdminSerializer, ProblemListSerializer, ProblemDetailSerializer, \
    ProblemTagSerializer, ProblemTagDetailSerializer


class ProblemTagAdminAPI(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = [permissions.IsAdminUser]


class ProblemTagAPI(viewsets.ReadOnlyModelViewSet):
    queryset = ProblemTag.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProblemTagSerializer
        else:
            return ProblemTagDetailSerializer


class ProblemAdminAPI(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProblemAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.filter(visible=True, is_public=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProblemListSerializer
        else:
            return ProblemDetailSerializer

    def list(self, request, *args, **kwargs):
        problems = ProblemAPI.queryset

        keyword = request.GET.get('keyword')
        tag_name = request.GET.get('tag')
        difficulty = request.GET.get('difficulty')
        if keyword:
            problems = problems.filter(title__contains=keyword)
        if tag_name:
            problems = problems.filter(tags__name=tag_name)
        if difficulty:
            problems = problems.filter(difficulty=difficulty)

        page = self.paginate_queryset(problems)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(problems, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def pick_one(self, request):
        problems = self.queryset
        count = problems.count()
        if count:
            pk = problems[random.randint(0, count - 1)].id
            return redirect(to='problem-detail', pk=pk)
        else:
            return Response(utils.response_dict(detail='题库中没有可选题目！'), status=status.HTTP_404_NOT_FOUND)


