from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Utilisateur générique django """
    pass


class Project(models.Model):
    """ Projet/produit/application en cours de développement ou de gestion """

    class Type(models.TextChoices):
        BACK_END = 'back-end'
        FRONT_END = 'front-end'
        IOS = 'iOS'
        ANDROID = 'Android'

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, verbose_name="Description")
    type = models.CharField(choices=Type.choices, max_length=10, verbose_name="Type")
    contributors = models.ManyToManyField(to=User, through='Contributor')


class Contributor(models.Model):
    """ Contributeur d'un projet (relation m2m User/Project) """

    class Permission(models.TextChoices):
        AUTEUR = 'Auteur'
        RESPONSABLE = 'Responsable'
        CREATEUR = 'Créateur'

    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(choices=Permission.choices, max_length=15, verbose_name="Permission")
    role = models.CharField(max_length=128, verbose_name="Rôle")

    class Meta:
        unique_together = ('user_id', 'project_id')


class Issue(models.Model):
    """ Problème d'un projet """

    class Tag(models.TextChoices):
        BUG = 'BUG'
        AMELIORATION = 'AMELIORATION'
        TACHE = 'TACHE'

    class Priority(models.TextChoices):
        FAIBLE = 'FAIBLE'
        MOYENNE = 'MOYENNE'
        ELEVEE = 'ELEVEE'

    class Status(models.TextChoices):
        A_FAIRE = 'A faire'
        EN_COURS = 'En cours'
        TERMINE = 'Terminé'

    title = models.CharField(max_length=128, verbose_name="Titre")
    desc = models.TextField(max_length=2048, verbose_name="Description")
    tag = models.CharField(choices=Tag.choices, max_length=15, verbose_name="Balise")
    priority = models.CharField(choices=Priority.choices, max_length=10, verbose_name="Priorité")
    status = models.CharField(choices=Status.choices, max_length=10, verbose_name="Statut")
    created_time = models.DateTimeField(auto_now_add=True)
    project_id = models.ForeignKey(to=Project, null=True, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, related_name='author')
    assignee_user_id = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, related_name='assign')


class Comment(models.Model):
    """ Commentaire d'un problème """

    description = models.TextField(max_length=2048, verbose_name="Description")
    created_time = models.DateTimeField(auto_now_add=True)
    issue_id = models.ForeignKey(to=Issue, null=True, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
