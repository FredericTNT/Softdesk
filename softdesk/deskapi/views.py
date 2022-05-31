from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.http import Http404

from deskapi.models import Project, Issue, Comment
from deskapi.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ProjectViewSetSerializer


def get_project(id):
    """ Vérification de l'existence et sélection d'un projet """
    try:
        return Project.objects.get(id=id)
    except Project.DoesNotExist:
        raise Http404


def get_issue(id_project, id):
    """ Vérification de l'existence dans l'arborescence project/issue et sélection d'un problème """
    try:
        return Issue.objects.filter(project_id=id_project).get(id=id)
    except Issue.DoesNotExist:
        raise Http404


def get_comment(id_project, id_issue, id):
    """ Vérification de l'existence dans l'arborescence project/issue/comment et sélection d'un commentaire """
    issues = Issue.objects.filter(project_id=id_project)
    try:
        return Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=id_issue)).get(id=id)
    except Comment.DoesNotExist:
        raise Http404


class ProjectList(APIView):
    """ Liste de tous les projets et création d'un projet """

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
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

    def get(self, request, *args, **kwargs):
        project = get_project(kwargs['id_project'])
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        project = get_project(kwargs['id_project'])
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = get_project(kwargs['id_project'])
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueList(APIView):
    """ Liste de tous les problèmes et création d'un problème """

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.filter(project_id=kwargs['id_project'])
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IssueSerializer(data=request.data)
        project = get_project(kwargs['id_project'])
        if serializer.is_valid():
            serializer.save(project_id=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """ Détail, modification et suppression d'un problème """

    def get(self, request, *args, **kwargs):
        issue = get_issue(kwargs['id_project'], kwargs['id_issue'])
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        issue = get_issue(kwargs['id_project'], kwargs['id_issue'])
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        issue = get_issue(kwargs['id_project'], kwargs['id_issue'])
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """ Liste de tous les commentaires et création d'un commentaire """

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.filter(project_id=kwargs['id_project'])
        comments = Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=kwargs['id_issue']))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        issue = get_issue(kwargs['id_project'], kwargs['id_issue'])
        if serializer.is_valid():
            serializer.save(issue_id=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """ Détail, modification et suppression d'un commentaire """

    def get(self, request, *args, **kwargs):
        comment = get_comment(kwargs['id_project'], kwargs['id_issue'], kwargs['id_comment'])
        serializer = IssueSerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment = get_comment(kwargs['id_project'], kwargs['id_issue'], kwargs['id_comment'])
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = get_comment(kwargs['id_project'], kwargs['id_issue'], kwargs['id_comment'])
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(ReadOnlyModelViewSet):

    serializer_class = ProjectViewSetSerializer

    def get_queryset(self):
        return Project.objects.all()
