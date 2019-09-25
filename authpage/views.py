from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pymongo import MongoClient


def home(request):
    return render(request, 'home.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        message = "Login Successful"
        return render(request, 'profile.html', {'message': message})
    else:
        messages.success(request, ('Invalid Credentials!!'))
        return redirect('home')


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.success(request, ('Username Already Exist!!'))
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.success(request, ('Email Already Exist!!'))
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, ('User Created!!'))
                return redirect('home')
        else:
            messages.success(request, ('MisMatch Password!!'))
            return redirect('register')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    messages.success(request, ('Logout Successful'))
    return redirect('home')


def check(request):
    if request.method == "POST":
        global username
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            return render(request, 'reset_pass.html')
        else:
            messages.success(request, ('Invalid Username!!'))
            return redirect('check')
    else:
        return render(request, 'checkusername.html')

def changePass(request):
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if password1 == password2:
        client = MongoClient(port=27017)
        db = client.login
        global username
        finding = db.auth_user.find_one({'username': username})
        db.auth_user.update_one({'_id': finding.get('_id')}, {'$inc': {'password': password1}})
        return redirect('home')
    else:
        messages.success(request, ('MisMatch Password'))
        return redirect('changePass')