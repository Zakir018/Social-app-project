from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile, Post
from django.contrib.auth.decorators import login_required



# Create your views here.
@ login_required
def index(request):
    
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.order_by('-created_at')

    context = {
        'profile':profile,
        'posts':posts
    }

        
    
    return render(request, 'social_app/index.html',context)

def signup(request):
    message = ''
    if request.method == "POST":
        first_name =request.POST.get('signup_firstname')
        last_name = request.POST.get('signup_lastname')
        username = request.POST.get('signup_username')
        email = request.POST.get('signup_email')
        password = request.POST.get('signup_password')
        repeat_password = request.POST.get('signup_confirm_password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        country = request.POST.get('country')

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
                username=username.lower(),
                email=email,
                password=password,
        )
            
        Profile.objects.create(
            user=register_user,
            first_name = first_name,
            last_name = last_name,
            email = email,
            age = age,
            gender = gender,
            country = country
        )
        register_user.save()
        return redirect('user_login')
            

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
def add_post(request):
    if request.post == 'POST':
        Post.objects.create(
            user = request.user,
            body = request.POST.get('body'),
            image = request.FILES.get('image')
        )
        Post.save()
        return redirect('index')


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
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        user = request.user

        # Get new values from POST request
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        profile_img = request.FILES.get('image')

        # Update the user's details
        if profile_img:
            profile.profile_picture = profile_img
        profile.first_name = new_first_name
        profile.last_name = new_last_name
        profile.email = new_email
        
        profile.save()

        context = {
            'my_dict':my_dict,
            'profile':profile
        }

    
    return render(request, 'social_app/profiles.html', {'profile':profile})

    
@login_required
def about(request):
    return render(request, 'social_app/about.html')
