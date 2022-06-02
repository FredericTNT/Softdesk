from rest_framework.permissions import BasePermission
from deskapi.models import Contributor


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        """ Vérifier l'accès aux utilisateurs administrateurs authentifiés """
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Vérifier l'accès à l'auteur de l'objet """
        print('objet', obj, type(obj).__name__, request.method, request.user)
        return obj.author_user_id == request.user


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        """ Vérifier l'accès aux contributeurs du projet """
        contributors = Contributor.objects.filter(project_id=view.kwargs['id_project'])
        for contributor in contributors:
            if contributor.user_id == request.user:
                return True
        return False
