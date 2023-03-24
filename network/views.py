from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Post
from .forms import createPost

def index(request):
    new_post = createPost()
    all_posts = Post.objects.all().order_by('-timestamp')
    
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = createPost(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            new_post = Post(content=content, user=request.user)
            new_post.save()
            return HttpResponseRedirect(reverse("index"))


    return render(request, "network/index.html", {
        "new_post": new_post,
        "posts": all_posts,
        "page_obj": page_obj
    })

def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_content = data["payload"]
        post_id = data["post_id"]
        post = Post.objects.get(id=post_id)
        post.content = new_content
        print(new_content, post_id)
        post.save()
        return JsonResponse({'status': 'success'})

def like(request, postId):
    if request.method == "POST":
        post = Post.objects.get(id=postId)
        likes = post.likes.all()
        

        if request.user in likes:
            post.likes.remove(request.user)
            likes = post.likes.all()
            numLikes = likes.count()
            print(likes, numLikes)
            return JsonResponse({'status': 'unliked', 'likes': numLikes})

        else:
            post.likes.add(request.user)
            likes = post.likes.all()
            numLikes = likes.count()
            print(likes, numLikes)
            return JsonResponse({'status': 'liked', 'likes': numLikes})
            

def profile(request, username):
    userProfile = User.objects.get(username=username)
    userPosts = Post.objects.filter(user=userProfile.id).order_by('-timestamp')
    userFollowing = userProfile.following.all()

    paginator = Paginator(userPosts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if request.method == "POST":
        status = request.POST["status"]
        if status == 'followed':
            userProfile.followers.add(request.user)
            request.user.following.add(userProfile)
            userProfile.save()
            request.user.save()

        elif status == 'unfollowed':
            userProfile.followers.remove(request.user)
            request.user.following.remove(userProfile)
            userProfile.save()
            request.user.save()
    
    userFollowers = userProfile.followers.all()
    is_following = False
    if request.user in userFollowers:
        is_following = True

    return render(request, "network/profile.html", {
        "userProfile": userProfile,
        "page_obj": page_obj,
        "userFollowers": userFollowers,
        "is_following": is_following,
        "userFollowing": userFollowing
    })

def following(request):
    uFollowing = request.user.following.all()
    posts = Post.objects.filter(user__in=uFollowing)

    return render(request, "network/following.html", {
        "posts": posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
