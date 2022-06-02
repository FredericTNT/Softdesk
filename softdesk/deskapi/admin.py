from django.contrib import admin
from deskapi.models import User, Project, Issue, Comment, Contributor


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project_id')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_id')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'project_id')


admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
