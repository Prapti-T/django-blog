from django.shortcuts import get_object_or_404
from .models import Post, Comment, Category
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .serializer import (
    SignupSerializer,
    LoginSerializer,
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Custom permission to only allow authors of an object to edit or delete it.
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
    
#Auth views:
#sign up
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Category views:
# List all categories
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# Create a new category
class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

#Post views:
#List all posts
class PostList(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_on')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['categories__name']
    permission_classes = [AllowAny]

#List posts by category
class PostByCategoryList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Post.objects.filter(categories__name__icontains=category_name).order_by('-created_on')

#Detail of a post including comments
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

#Create a new post
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

#Update post
class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

#Delete post
class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

#Comment views:
#List comments for a post
class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post__id=post_id).order_by('-created_on')

#Get single comment
class CommentDetail(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        post_pk = self.kwargs['post_pk']
        comment_pk = self.kwargs['pk']
        return get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    
#Create comment
class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post)
    
#Update comments    
class CommentUpdate(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

#Delete comments
class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]