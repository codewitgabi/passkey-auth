from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import auth
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# user object
User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "HANKO_API_URL": settings.HANKO_API_URL
    }
    return render(request, "myapp/index.html", context)


@api_view(["POST"])
def create_user(request: HttpRequest) -> Response:
    if request.method == "POST":
        userId = request.data.get("userId")
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            id=userId, email=email, username=" ", password=" "
        )
        user.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


def complete_profile(request: HttpRequest, userId) -> HttpResponse:
    user = get_object_or_404(User, id=userId)

    if user.username not in ["", " "]:
        # authenticate request

        user = auth.authenticate(userId= user.id, email=user.email)

        if user is not None:
            auth.login(request, user)

        return redirect("myapp:app")

    if request.method == "POST":
        username = request.POST.get("username")

        user.username = username
        user.save()

        # authenticate request

        user = auth.authenticate(userId=user.id, email=user.email)

        if user is not None:
            auth.login(request, user)

        return redirect("myapp:app")
    return render(request, "myapp/complete-profile.html")


def app(request: HttpRequest) -> HttpResponse:
    print("USER", request.user)
    context = {
        "HANKO_API_URL": settings.HANKO_API_URL
    }
    return render(request, "myapp/logout.html", context)
