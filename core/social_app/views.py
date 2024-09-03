from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile, Post, Comments
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timesince import timesince


# Create your views here.
@ login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.order_by('-created_at')
    for post in posts:
        post.count = Comments.objects.filter(post=post).count()

    # context dictionary
    context = {
        'profile': profile,
        'posts': posts,
    }
    
    return render(request, 'social_app/index.html', context)


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
                user = register_user,
                first_name = first_name,
                last_name = last_name,
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
    if request.method == 'POST':
        Post.objects.create(
            user = request.user,
            body = request.POST.get('body'),
            image = request.FILES.get('image')
        )
        return redirect('index')


@login_required
def edit_post(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        page = request.POST.get('page')
        body =request.POST.get('body')
        image = request.FILES.get('image')
        post = Post.objects.get(id = id)
        if image:
            post.image = image
        post.body = body
        post.save()

        return redirect(page)

@login_required
def delete_post(request, pk, page):
    Post.objects.get(id = pk).delete()
    return redirect(page)

def add_comments(request) :
    if request.method == 'POST':
        id = request.POST.get('id')
        page = request.POST.get('page')
        body = request.POST.get('comment_body')
        post = Post.objects.get(id=id)
        
        comments = Comments.objects.create(
            user =request.user,
            post = post,
            body = body,
        )
        comments.save()
        return redirect(page)


def fetch_comments(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comments.objects.filter(post=post).values(
        'body',
        'user__profile__profile_picture',
        'user__profile__first_name',
        'user__profile__last_name',
        'created_at'
        )

    comments_data = []
    for comment in comments:
        item = {
            "body": comment['body'],
            "image": f"/media/{comment['user__profile__profile_picture']}",
            "name": f"{comment['user__profile__first_name']} {comment['user__profile__last_name']}",
            "time": timesince(comment['created_at'])
        }
        comments_data.append(item)
    return JsonResponse({'status': 'success', 'comments': comments_data})


"""
comment_dict = {"body": "hi there"}
comment_dict['body'] = "hi there"

"""


@login_required
def friends(request):
    return render(request, 'social_app/friends.html')


@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    for post in posts:
        post.count = Comments.objects.filter(post=post).count()


    if request.method == 'POST':
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        age = request.POST.get('age')
        profile_img = request.FILES.get('image')


        if profile_img:
            profile.profile_picture = profile_img
        profile.first_name = new_first_name
        profile.last_name = new_last_name
        profile.gender = gender
        profile.country = country
        profile.age = age


        
        profile.save()

    context = {
        'profile': profile,
        'posts': posts
    }
    return render(request, 'social_app/profiles.html',context)


@login_required
def about(request):
    return render(request, 'social_app/about.html')
