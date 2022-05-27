from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.http import Http404

from deskapi.models import User, Project, Issue, Comment
from deskapi.serializers import ProjectListSerializer, IssueListSerializer, CommentListSerializer
from deskapi.serializers import ProjectDetailSerializer
from deskapi.serializers import ProjectDetailViewSetSerializer


class ProjectListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__in=User.objects.filter(id=request.user.id))
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        id_project = kwargs.get('id_project', None)
        project = self.get_object(id_project)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id_project = kwargs.get('id_project', None)
        project = Project.objects.get(id=id_project)
        serializer = ProjectDetailSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueAPIView(APIView):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__in=User.objects.filter(id=request.user.id))
        issues = Issue.objects.filter(Q(project_id__in=projects) & Q(project_id=kwargs['id_project']))
        id_issue = kwargs.get('id_issue', None)
        if id_issue:
            issues = issues.filter(id=id_issue)
        serializer = IssueListSerializer(issues, many=True)
        return Response(serializer.data)


class CommentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__in=User.objects.filter(id=request.user.id))
        issues = Issue.objects.filter(Q(project_id__in=projects) & Q(project_id=kwargs['id_project']))
        comments = Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=kwargs['id_issue']))
        id_comment = kwargs.get('id_comment', None)
        if id_comment:
            comments = comments.filter(id=id_comment)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)


class ProjectViewSet(ReadOnlyModelViewSet):

    serializer_class = ProjectDetailViewSetSerializer

    def get_queryset(self):
        return Project.objects.all()
