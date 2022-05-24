from rest_framework.serializers import ModelSerializer
from deskapi.models import Project, Issue, Comment, User


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue_id']


class CommentDetailViewSetSerializer(ModelSerializer):

    author_user_id = UserListSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user_id']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'status', 'project_id']


class IssueDetailViewSetSerializer(ModelSerializer):

    author_user_id = UserListSerializer(many=False)
    assignee_user_id = UserListSerializer(many=False)
    comments = CommentDetailViewSetSerializer(many=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'created_time', 'author_user_id',
                  'assignee_user_id', 'comments']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title']


class ProjectDetailViewSetSerializer(ModelSerializer):

    contributors = UserListSerializer(many=True)
    issues = IssueDetailViewSetSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors', 'issues']
