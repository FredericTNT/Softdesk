from rest_framework.serializers import ModelSerializer, ValidationError
from deskapi.models import Project, Issue, Comment, User


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time']


class CommentViewSetSerializer(ModelSerializer):

    author_user_id = UserListSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user_id']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'created_time']


class IssueViewSetSerializer(ModelSerializer):

    author_user_id = UserListSerializer(many=False)
    assignee_user_id = UserListSerializer(many=False)
    comments = CommentViewSetSerializer(many=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'created_time', 'author_user_id',
                  'assignee_user_id', 'comments']


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError('Projet existant avec le même titre')
        return value


class ProjectViewSetSerializer(ModelSerializer):

    contributors = UserListSerializer(many=True)
    issues = IssueViewSetSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors', 'issues']
