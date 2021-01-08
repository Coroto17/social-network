from typing import Dict
from .models import Post
from django.core.paginator import Paginator


def create_pagination(request, user=None):
    """Creates the context for paginated posts"""
    if user:
        posts = Post.objects.filter(author=user).order_by("-timestamp")
    else:
        posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 5)
    current_page = request.GET.get("page", 1)
    page_obj = paginator.get_page(current_page)
    context = {"page_obj": page_obj}
    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
        context.update({"liked_posts": liked_posts})
    return context
