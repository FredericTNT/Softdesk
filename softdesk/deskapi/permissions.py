from rest_framework.permissions import BasePermission
from deskapi.models import Contributor


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        """ Vérifier si l'utilisateur est authentifié et administrateur """
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Vérifier si l'utilisateur est l'auteur de l'objet pour les méthodes autres que GET """
        if request.method == 'GET':
            return True
        return obj.author_user_id == request.user


class IsProjectAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Vérifier si l'utilisateur est l'auteur du projet pour les méthodes autres que GET """
        if request.method == 'GET':
            return True
        for contributor in Contributor.objects.filter(user_id__in=obj.contributors.all(), permission='Auteur'):
            if contributor.user_id == request.user:
                return True
        return False


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        """ Vérifier si l'utilisateur est un contributeur du projet """
        for contributor in Contributor.objects.filter(project_id=view.kwargs['id_project']):
            if contributor.user_id == request.user:
                return bool(request.user and request.user.is_authenticated)
        return False


class IsContributorAuthor(BasePermission):

    def has_permission(self, request, view):
        """ Vérifier si l'utilisateur est l'auteur du projet pour les méthodes autres que GET """
        if request.method == 'GET':
            return True
        for contributor in Contributor.objects.filter(project_id=view.kwargs['id_project']):
            if (contributor.user_id == request.user) and (contributor.permission == 'Auteur'):
                return bool(request.user and request.user.is_authenticated)
        return False
