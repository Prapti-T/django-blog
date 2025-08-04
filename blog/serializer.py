from rest_framework import serializers
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_on', 'post']

class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    author = serializers.ReadOnlyField(source='author.username')  # Show author username, read-only

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_on', 'last_modified', 'categories', 'comments']

