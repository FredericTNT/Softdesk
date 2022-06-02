from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.shortcuts import get_object_or_404

from deskapi.models import Project, Issue, Comment, User
from deskapi.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ProjectViewSetSerializer
from deskapi.permissions import IsAdminAuthenticated, IsAuthor, IsContributor


class ProjectList(APIView):
    """ Liste de tous les projets et création d'un projet """

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__in=User.objects.filter(id=request.user.id))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """ Détail, modification et suppression d'un projet """

    permission_classes = [IsContributor]

    def get_object(self):
        project = get_object_or_404(Project, id=self.kwargs['id_project'])
        self.check_object_permissions(self.request, project)
        return project

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueList(APIView):
    """ Liste de tous les problèmes et création d'un problème """

    permission_classes = [IsContributor]

    def tree_project(self):
        project = get_object_or_404(Project, id=self.kwargs['id_project'])
        return project

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.filter(project_id=kwargs['id_project'])
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IssueSerializer(data=request.data)
        project = self.tree_project()
        if serializer.is_valid():
            serializer.save(project_id=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """ Détail, modification et suppression d'un problème """

    permission_classes = [IsContributor]

    def get_object(self):
        queryset = Issue.objects.filter(project_id=self.kwargs['id_project'])
        issue = get_object_or_404(queryset, id=self.kwargs['id_issue'])
        self.check_object_permissions(self.request, issue)
        return issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        issue = self.get_object()
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """ Liste de tous les commentaires et création d'un commentaire """

    permission_classes = [IsContributor]

    def tree_issue(self):
        queryset = Issue.objects.filter(project_id=self.kwargs['id_project'])
        issue = get_object_or_404(queryset, id=self.kwargs['id_issue'])
        return issue

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.filter(project_id=kwargs['id_project'])
        comments = Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=kwargs['id_issue']))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        issue = self.tree_issue()
        if serializer.is_valid():
            serializer.save(issue_id=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """ Détail, modification et suppression d'un commentaire """

    permission_classes = [IsContributor]

    def get_object(self):
        issues = Issue.objects.filter(project_id=self.kwargs['id_project'])
        queryset = Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=self.kwargs['id_issue']))
        comment = get_object_or_404(queryset, id=self.kwargs['id_comment'])
        self.check_object_permissions(self.request, comment)
        return comment

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = IssueSerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(ReadOnlyModelViewSet):

    serializer_class = ProjectViewSetSerializer
#    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Project.objects.all()
