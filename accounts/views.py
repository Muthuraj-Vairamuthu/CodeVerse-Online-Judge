from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("/problems/")  # ✅ Redirect here
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("/auth/login/")

    return render(request, "accounts/register.html")

def logout_view(request):
    logout(request)
    return redirect("/auth/login/")
from django.http import HttpResponse

def home_view(request):
    return render(request, "accounts/home.html")