from django.urls import path
from .views import (
    SignupView, 
    LoginView,
    PostList,
    PostByCategoryList,
    CategoryCreate,
    CategoryList,
    PostDetail,
    PostCreate,
    PostUpdate,
    PostDelete,
    CommentList,
    CommentCreate,
    CommentUpdate,
    CommentDelete, 
    CommentDetail
    )


urlpatterns = [
    #Authentication urls:
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    #Categories urla
    path('categories/', CategoryList.as_view(), name='category-list'),  # GET list
    path('categories/', CategoryCreate.as_view(), name='category-create'),  # POST create

    # Posts urls
    path('posts/', PostList.as_view(), name='post-list'),  # GET list of all posts
    path('posts/category/<str:category>/', PostByCategoryList.as_view(), name='posts-by-category'), #GET list of posts by category
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),  # GET detail of one post
    path('posts/<int:pk>/', PostUpdate.as_view(), name='post-update'),  # PUT update
    path('posts/<int:pk>/', PostDelete.as_view(), name='post-delete'),  # DELETE delete
    path('posts/', PostCreate.as_view(), name='post-create'),  # POST create

    #Comments urls (nested under posts)
    path('posts/<int:post_pk>/comments/', CommentList.as_view(), name='comment-list'),  # GET list of all comments on a post
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),#GET single comment
    path('posts/<int:post_pk>/comments/', CommentCreate.as_view(), name='comment-create'),  # POST create
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentUpdate.as_view(), name='comment-update'),  # PUT update
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentDelete.as_view(), name='comment-delete'),  # DELETE delete
]