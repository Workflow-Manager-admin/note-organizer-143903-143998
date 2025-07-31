from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Note


# PUBLIC_INTERFACE
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    # PUBLIC_INTERFACE
    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    # PUBLIC_INTERFACE
    def create(self, validated_data):
        """
        Create new user according to validated data.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating an existing user.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # PUBLIC_INTERFACE
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        data['user'] = user
        return data


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note CRUD operations.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at',
            'owner', 'folder', 'is_favorite', 'is_archived'
        ]
