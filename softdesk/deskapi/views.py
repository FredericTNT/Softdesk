from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.shortcuts import get_object_or_404

from authentication.models import User
from deskapi.models import Project, Issue, Comment, Contributor
from deskapi.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from deskapi.serializers import ProjectViewSetSerializer
from deskapi.permissions import IsAdminAuthenticated, IsAuthor, IsProjectAuthor, IsContributor, IsContributorAuthor


class ProjectList(APIView):
    """ Liste de tous les projets (GET) et création d'un projet (POST) """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__in=User.objects.filter(id=request.user.id))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            project = get_object_or_404(Project, id=serializer.data['id'])
            Contributor.objects.create(user_id=request.user, project_id=project, permission='Auteur', role='A définir')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """ Détail (GET), modification (PUT) et suppression (DELETE) d'un projet """

    permission_classes = [IsContributorAuthor]

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


class ContributorList(APIView):
    """ Liste de tous les contributeurs (GET) et ajout d'un contributeur (POST) """

    permission_classes = [IsContributor]

    def tree_project(self):
        project = get_object_or_404(Project, id=self.kwargs['id_project'])
        return project

    def get(self, request, *args, **kwargs):
        contributors = Contributor.objects.filter(project_id=kwargs['id_project'])
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        project = self.tree_project()
        if serializer.is_valid():
            serializer.save(project_id=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorDelete(APIView):
    """ Suppression (DELETE) d'un contributeur """

    permission_classes = [IsContributorAuthor]

    def get_object(self):
        queryset = Contributor.objects.filter(project_id=self.kwargs['id_project'])
        contributor = get_object_or_404(queryset, user_id=self.kwargs['id_user'])
        self.check_object_permissions(self.request, contributor)
        return contributor

    def delete(self, request, *args, **kwargs):
        contributor = self.get_object()
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueList(APIView):
    """ Liste de tous les problèmes (GET) et création d'un problème (POST) """

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
            serializer.save(project_id=project, author_user_id=request.user, assignee_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """ Détail (GET), modification (PUT) et suppression (DELETE) d'un problème """

    permission_classes = [IsContributor, IsAuthor]

    def get_object(self):
        queryset = Issue.objects.filter(project_id=self.kwargs['id_project'])
        issue = get_object_or_404(queryset, id=self.kwargs['id_issue'])
        self.check_object_permissions(self.request, issue)
        return issue

    def IsProjectContributor(self, user):
        """ Vérifier si l'utilisateur est un contributeur du projet """
        for contributor in Contributor.objects.filter(project_id=self.kwargs['id_project']):
            if contributor.user_id == user:
                return True
        return False

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid() and self.IsProjectContributor(serializer.validated_data['assignee_user_id']) and\
                self.IsProjectContributor(serializer.validated_data['author_user_id']):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        issue = self.get_object()
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """ Liste de tous les commentaires (GET) et création d'un commentaire (POST) """

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
            serializer.save(issue_id=issue, author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """ Détail (GET), modification (PUT) et suppression (DELETE) d'un commentaire """

    permission_classes = [IsContributor, IsAuthor]

    def get_object(self):
        issues = Issue.objects.filter(project_id=self.kwargs['id_project'])
        queryset = Comment.objects.filter(Q(issue_id__in=issues) & Q(issue_id=self.kwargs['id_issue']))
        comment = get_object_or_404(queryset, id=self.kwargs['id_comment'])
        self.check_object_permissions(self.request, comment)
        return comment

    def IsProjectContributor(self, user):
        """ Vérifier si l'utilisateur est un contributeur du projet """
        for contributor in Contributor.objects.filter(project_id=self.kwargs['id_project']):
            if contributor.user_id == user:
                return True
        return False

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid() and self.IsProjectContributor(serializer.validated_data['author_user_id']):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(ReadOnlyModelViewSet):
    """ Liste détaillée des projets / problèmes / commentaires (réservée aux administrateurs) """

    queryset = Project.objects.all()
    serializer_class = ProjectViewSetSerializer
    permission_classes = [IsAdminAuthenticated]
