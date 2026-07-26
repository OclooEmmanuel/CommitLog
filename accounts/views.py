from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname',"").strip()
        lastname = request.POST.get('lastname', "").strip()
        username = request.POST.get('username',"").strip()
        email = request.POST.get('email', "").strip()
        password =request.POST.get('password1')
        confirm_password = request.POST.get('password2')


        if password != confirm_password:
            messages.error(request,"Passwords do not match!")
            return redirect("register")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'username already exists!!')
            return redirect('register')

        user = User.objects.create_user(
            first_name =firstname,
            last_name = lastname,
            email=email,
            username=username,
            password=password,
        )

        user.save()
        return redirect("login")
    return render(request, "register.html")



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if not user is None:
            login(request,user)
            messages.success(request,f"welcome back {user.username}!")
            return redirect('blog:post_list')
        else:
            messages.error(request, "Invalid usrname or password.")
            return redirect('login')

    return render(request, "login.html")


def logout_view(request):
        logout(request)
        messages.info(request, "You have been loged out.")
        return redirect("login")

