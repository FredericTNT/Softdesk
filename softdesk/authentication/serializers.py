from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from django.contrib.auth.password_validation import validate_password
from authentication.models import User


class RegisterSerializer(ModelSerializer):
    """ Serializer du modèle User avec contrôle du mot de passe selon les règles de validation définies dans
        Django et confirmation du mot de passe par double saisie """

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({'password': 'Les deux mots de passe ne sont pas identiques'})
        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
