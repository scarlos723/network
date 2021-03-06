
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.compose_post, name="compose_post"),
    path("profile/<str:id>", views.show_user, name="show_user"),
    path("follow/<str:id>", views.follow_to, name="follow_to"),
    path("following/<str:id>", views.following_to, name="following_to"),
    path("update", views.update_post, name="update_post"),
    path("like", views.add_like, name="add_like"),
    path("unlike",views.remove_like,name="remove_like"),
    path("unfollow/<str:id>", views.unfollow_to, name="unfollow_to")

]
