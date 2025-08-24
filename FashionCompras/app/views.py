from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auth
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .data import popular_items, Cart_items

@login_required(login_url='login_page')  # if not logged in → redirect to /login/
def home(request):
    context = {
        'popular_items': popular_items
        }
    return render(request, 'home.html' , context)




def signup_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user already exists
        if Auth.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login instead.")
            return redirect("login_page")

        # Create new user with hashed password
        user = Auth.objects.create(
            email=email,
            password=make_password(password)   # hash password securely
        )

        # Log the user in immediately
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "sign_up.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Auth.objects.get(email=email)
            if check_password(password, user.password):  # secure check
                login(request, user)  # create session
                return redirect("home")
            else:
                messages.error(request, "Incorrect password!")
        except Auth.DoesNotExist:
            messages.error(request, "Invalid Email or Password")

        return redirect("login_page")

    return render(request, "login.html")

def Logout(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("login_page")

    return render(request, "Logout.html")


def Cart(request):
    context = {
        'Cart_items': Cart_items
        }
    return render(request, "cart.html",context)

def Deals(request):
    
    return render(request, "Deals.html")

def Item(request):
    return render(request, "item.html")


def Contact(request):
    return render(request, "Contact.html")


