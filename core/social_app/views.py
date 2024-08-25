from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@ login_required
def index(request):
    my_dict = {
        'name1' : 'Zakir khan',
        'name2' : 'Irshad Husian',
        'name3' : 'Sohrab Khan',
        'name4' : 'Khalid Ali Khan',
        'name5' : 'Bilal Khan',
        'name6' : 'Umair Khan',
        'name7' : 'Omar Akhtar'
    }

        
    
    return render(request, 'social_app/index.html', {'my_dict': my_dict})

def signup(request):
    message = ''
    if request.method == "POST":
        first_name =request.POST.get('signup_firstname')
        last_name = request.POST.get('signup_lastname')
        username = request.POST.get('signup_username')
        email = request.POST.get('signup_email')
        password = request.POST.get('signup_password')
        repeat_password = request.POST.get('signup_confirm_password')

        if User.objects.filter(username=username).exists():
            message = "username already regester"

        elif User.objects.filter(email=email).exists():
            message = "email already regester"

        elif len(password) < 8 :
            message = "password must be 8 charachter long"

        elif password != repeat_password :
            message = "password and repeat password must be same"

        else:
            register_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username.lower(),
                email=email,
                password=password,
        )
            
        Profile.objects.create(
            user=register_user,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        register_user.save()
            

    return render(request, 'social_app/signup.html', {'message':message})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return  redirect('index')

    return render(request, 'social_app/user_login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def photos(request):
    return render(request, 'social_app/photos.html')

@login_required
def friends(request):
    return render(request, 'social_app/friends.html')

@login_required
def profile(request):
    my_dict = {
        'name1' : 'Zakir khan',
        'name2' : 'Irshad Husian',
        'name3' : 'Sohrab Khan',
        'name4' : 'Khalid Ali Khan',
        'name5' : 'Bilal Khan',
        'name6' : 'Umair Khan',
        'name7' : 'Omar Akhtar'
    }
    return render(request, 'social_app/profiles.html', {'my_dict': my_dict})

@login_required
def about(request):
    return render(request, 'social_app/about.html')
