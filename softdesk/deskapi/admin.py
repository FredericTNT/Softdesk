from django.contrib import admin
from deskapi.models import User, Project, Issue, Comment


class IssueAdmin(admin.ModelAdmin):
    issue_display = ('title', 'project_id')


class CommentAdmin(admin.ModelAdmin):
    comment_display = ('id', 'issue_id')


admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
