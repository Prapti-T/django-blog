from django.shortcuts import render, redirect, get_object_or_404
    #Helps to render HTML template with the given context
from django.http import HttpResponseRedirect
    #redirect the user to a different URL.
from blog.models import Post, Comment, Category
    #These are the models
from blog.forms import CommentForm, PostForm
    #form class for handling comments.
from blog.serializer import PostSerializer, CategorySerializer, CommentSerializer
from rest_framework import viewsets

#Function for handling the blog index page, which lists all blog posts.
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)
     #retrieves all Post obj from db and order DESC, pass to template


#Function for handling the category page, which lists blog posts for a specific category.
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains = category).order_by("-created_on")
    context = {
        'category' : category,
        'posts' : posts,
    }
    return render(request, "blog/category.html", context)
    #Filters Post objects that have a category name containing the given category, orders them DESC, passes posts and category name to template


#Function for handling detail view of a single blog post, including comments and handling new comment submissions.
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)  #retrieves post obj using primary key
    form = CommentForm()

    #when user submits form, save to db and update comment list
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data['author'],
                body = form.cleaned_data['body'],
                post = post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)


#Create new posts
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
            )
            post.save()
            post.categories.set(form.cleaned_data['categories'])
            return redirect('blog_detail', pk = post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

#Update post
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

# Delete post
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')  # or your blog list view
    return render(request, 'blog/post_confirm_delete.html', {'post': post})