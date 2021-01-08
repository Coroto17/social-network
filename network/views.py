import json
from django.core.paginator import Paginator
from network.utils import create_pagination
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post


def index(request):
    # start building the paginated post context
    context = create_pagination(request)
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"), status=302)
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)

        if not username or not email:
            return render(
                request,
                "network/register.html",
                {"message": "username and email fields required"},
            )

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        post_content = request.POST.get("post_content", None)

        if user and post_content:
            Post.objects.create(author=user, content=post_content.strip())
        return HttpResponseRedirect(reverse("index"))


# like post
@login_required
def post(request, post_id):
    # retieve Post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    # retrieve user if authenticated
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    else:
        user = None

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("action") == "like":
            if user in post.liked_by.all():
                post.liked_by.remove(user)
                post.number_of_likes -= 1
                liked = False
            else:
                post.liked_by.add(user)
                post.number_of_likes += 1
                liked = True
            post.save()
            return JsonResponse(
                {"likes": post.number_of_likes, "liked": liked}, status=200
            )
        elif data.get("action") == "edit":
            new_content = data.get("newText", None)
            if new_content and new_content != post.content:
                try:
                    post.content = new_content
                except IntegrityError:
                    return JsonResponse({"error": "post not found"}, status=404)
                post.save()
                return JsonResponse(
                    {"message": "change successful", "post_content": new_content},
                    status=200,
                )
            else:
                return HttpResponse(status=204)


# All posts view
def all_posts(request):
    context = create_pagination(request)
    return render(request, "network/allposts.html", context)


# Profile page view
def profile_page(request, user_id):
    if request.method == "PUT":

        data = json.loads(request.body)
        if data.get("action") == "follow":
            user_to_query = User.objects.get(username=data.get("user"))
            print(user_to_query.get_followers_count())
            # follow
            if request.user not in user_to_query.followers.all():
                request.user.following.add(user_to_query)
                return JsonResponse(
                    {
                        "following": True,
                        "followers_count": user_to_query.get_followers_count(),
                    },
                    status=200,
                )
            # unfollow
            else:
                request.user.following.remove(user_to_query)
                return JsonResponse(
                    {
                        "following": False,
                        "followers_count": user_to_query.get_followers.count(),
                    }
                )

    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        user = None
    a_follows_b = request.user in user.followers.all()
    context = {
        "a_follows_b": a_follows_b,
        "username": user.username,
        "user_id": user.id,
        "join_date": user.get_join_date(),
        "user_posts": user.get_posts(),
        "following": user.get_following_count(),
        "followers": user.get_followers_count(),
    }
    if user.get_posts():
        context.update(create_pagination(request, user))

    return render(request, "network/profilepage.html", context)


# Following page
@login_required
def following(request, user_id):
    posts = []
    context = {}
    # get first 50 posts of users i follow
    user = request.user
    if user.following.all():
        posts = Post.objects.filter(author__in=user.following.all()).order_by(
            "-timestamp"
        )[:50]
        # create a custom pagination from the posts list
        paginator = Paginator(posts, 5)
        current_page = request.GET.get("page", 1)
        page_obj = paginator.get_page(current_page)
        context = {"page_obj": page_obj}
        liked_posts = user.liked_posts.all()
        context.update({"liked_posts": liked_posts})

    return render(request, "network/following.html", context)


# Page Not Found
def handle404(request, exception):
    return render(request, "network/404.html", status=404)
