from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new_post"),
    path("posts", views.all_posts, name="all_posts"),
    path("posts/<str:post_id>", views.post, name="post"),
    path("users/<str:user_id>", views.profile_page, name="profile"),
    path("users/<str:user_id>/following", views.following, name="following"),
]
