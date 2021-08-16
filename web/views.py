from django.shortcuts import render

from posts.models import Post

def home(request):
    return render(request, "web/index.html")

def about(request):
    return render(request, "web/about.html")

def post(request, post_id):
    post = Post.get_by_uuid(post_id)
    context = {"post": post}
    return render(request, "web/post.html", context)
