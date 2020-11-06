
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.compose_post, name="compose_post"),
    path("profile/<str:id>", views.show_user, name="show_user"),
    path("follow/<str:id>", views.follow_to, name="follow_to")
]
