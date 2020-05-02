import os
import random
from django.shortcuts import redirect
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from XDOJ import settings
from account import perms
from problem.utils import process_zip, ZipException
from utils import tools
from problem.models import Problem, ProblemTag
from problem.serializers import ProblemAdminSerializer, ProblemListSerializer, ProblemDetailSerializer, \
    ProblemTagSerializer, ProblemTagDetailSerializer, TestCaseUploadForm
from utils.tools import get_dict, rand_str
from utils.responses import SuccessResponse, ErrorResponse


class ProblemTagAdminAPI(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = [perms.IsAdminUser]


class ProblemTagAPI(viewsets.ReadOnlyModelViewSet):
    queryset = ProblemTag.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProblemTagSerializer
        else:
            return ProblemTagDetailSerializer

# ====================================================================


class ProblemAdminAPI(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemAdminSerializer
    permission_classes = [perms.IsAdminUser]

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
            return Response(tools.get_dict(detail='题库中没有可选题目！'), status=status.HTTP_404_NOT_FOUND)


class TestCaseAdminAPI(generics.GenericAPIView):
    def get(self, request):
        # TODO 待完成：下载测试点文件
        return ErrorResponse(msg='暂不支持测试点下载', http_status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        form = TestCaseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
        else:
            return ErrorResponse("文件上传失败！")

        # TODO 有待改进：被上传文件重命名防止冲突
        zip_file = f"{settings.TEMP_ROOT}{rand_str()}.zip"
        with open(zip_file, "wb") as f:
            for chunk in file:
                f.write(chunk)

        try:
            info, test_case_id = process_zip(file)
        except ZipException as e:
            return ErrorResponse(msg=e.msg, http_status=status.HTTP_400_BAD_REQUEST)
        finally:
            os.remove(zip_file)
        return SuccessResponse(msg=get_dict(id=test_case_id, info=info))
