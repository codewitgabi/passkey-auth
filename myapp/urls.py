from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("create-user/", views.create_user, name="create_user"),
    path(
        "complete-profile/<uuid:userId>/",
        views.complete_profile,
        name="complete_profile",
    ),
    path("app/", views.app, name="app"),
]
