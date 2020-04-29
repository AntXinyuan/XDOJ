from rest_framework import viewsets, permissions
from problem.models import Problem
from problem.serializers import ProblemAdminSerializer, ProblemListSerializer, ProblemSerializer


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
            return ProblemSerializer
