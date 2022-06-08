from rest_framework.serializers import ModelSerializer
from authentication.models import User
from deskapi.models import Project, Issue, Comment, Contributor


class UserViewSetSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class CommentViewSetSerializer(ModelSerializer):

    author_user_id = UserViewSetSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user_id']


class IssueViewSetSerializer(ModelSerializer):

    author_user_id = UserViewSetSerializer(many=False)
    assignee_user_id = UserViewSetSerializer(many=False)
    comments = CommentViewSetSerializer(many=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'created_time', 'author_user_id',
                  'assignee_user_id', 'comments']


class ProjectViewSetSerializer(ModelSerializer):

    contributors = UserViewSetSerializer(many=True)
    issues = IssueViewSetSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors', 'issues']


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'created_time',
                  'author_user_id', 'assignee_user_id']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user_id']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'permission', 'role']

