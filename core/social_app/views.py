from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Social_group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timesince import timesince


# Create your views here.
@ login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    friends = Profile.objects.all()
    posts = Post.objects.order_by('-created_at')
    groups = Social_group.objects.all()
    print(groups)
    for post in posts:
        post.liked_by_user = post.is_liked_by_user(request.user)
        
    # context dictionary
    context = {
        'profile': profile,
        'posts': posts,
        'friends':friends,
        'groups':groups
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
def setting(request):
    user = request.user

    return render(request, 'social_app/setting.html')


@login_required
def edit_personal_information (request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        user.username = username
        user.email = email
        user.save()

        return redirect('setting')
        
    
@login_required
def change_user_password(request):
    message = 'ok g'
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(old_password):
            message = 'Current password incorrent'

        elif new_password != confirm_password :
            message = 'New password and confirm password are not the same'

        else:
            user.set_password(new_password)
            user.save()
            
            return redirect('setting')
        
    
    return render(request, 'social_app/setting.html',{'message': message})


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()

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


login_required
def add_comments(request) :
    message = ''
    if request.method == 'POST':
        id = request.POST.get('id')
        page = request.POST.get('page')
        body = request.POST.get('comment_body')
        post = Post.objects.get(id=id)
        
        if body == "":
            message = 'comment is emty'
        else:
            comments = Comment.objects.create(
                user =request.user,
                post = post,
                body = body,
            )
        comments.save()
        return redirect(page)


login_required
def fetch_comments(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post).values(
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


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)
    user = request.user
    liked = False
    like = Like.objects.filter(user=user, post=post).first()

    if like:
        like.delete()
        message = "You unlike this post"

    else:
        Like.objects.create(user = user, post = post)
        liked = True
        message = "You like this post"

    response_data = {
        "liked":liked, 
        "total_likes": post.likes.count(),
        "message":message
        }
    
    return JsonResponse(response_data)


@login_required
def create_group(request):
    if request.method == "POST":
        group = Social_group.objects.create(
            user = request.user,
            name = request.POST.get('group_name'),
            description = request.POST.get('group_description'),
            profile_img = request.FILES.get('group_profile'),
            cover_img = request.FILES.get('group_coverpic')
        )
        group.save()
        return redirect('group', group.id )




@login_required
def group(request, pk):
    print(pk)
    group = get_object_or_404(Social_group, id=pk)
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'social_app/group.html', {'group':group, 'profile':profile})

@login_required
def friends(request):
    return render(request, 'social_app/friends.html')


@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.is_liked_by_user(request.user)


    if request.method == 'POST':
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        age = request.POST.get('age')
        profile_img = request.FILES.get('profile_image')
        cover_img = request.FILES.get('cover_image')


        if profile_img:
            profile.profile_picture = profile_img
        if cover_img:
            profile.cover_picture = cover_img
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
