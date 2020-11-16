from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Followers, Like


def index(request):
    
    posts = Post.objects.all().order_by('-date')
    new_posts=[]
    for one_post in posts:
        try:
            like = Like.objects.filter(user=request.user, post=one_post) 
        except:
            like=None
            print("Error al obtener like")

        if like:
            one_post.verify_like = True
        else:
            one_post.verify_like = False

        new_posts.append(one_post)
        

    paginator = Paginator(new_posts,10)
    page = request.GET.get('page')
        
    all_posts = paginator.get_page(page)
    
    return render(request, "network/index.html", { "posts":all_posts})


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

def compose_post(request):

    if request.method == "POST":
        content = request.POST["text"]
        user = User.objects.get(pk = request.POST["id"])
        
        try:
            post = Post.objects.create(user=user, text=content, likes= 0)
            post.save()
        except :
            print("Algo salio mal")

        print("se creo un post")
        return HttpResponseRedirect(reverse("index"))
        
    HttpResponseRedirect(reverse("index"))


def show_user(request, id):

    
    user_prof = User.objects.get(pk=id)

    follow_count = Followers.objects.filter(user=user_prof).count()
    all_posts = Post.objects.filter(user=user_prof).order_by('-date')
    followed_count = Followers.objects.filter(follower=user_prof).count()
    all_p = []
    
    #verificar si existe relacion 1 existe, 0 no existe
    relation = Followers.objects.filter(user=user_prof , follower=request.user).count()

    try:
        print(len(all_posts))
    except (TypeError):
        all_p.append(Post.objects.get(user=user_prof))
        all_posts = all_p


    like_posts_pag=[]
    
    for one_post in all_posts:
        try:
            like = Like.objects.filter(user=request.user, post=one_post) 
        except:
            like=None
            print("Error al obtener like")

        if like:
            one_post.verify_like = True
        else:
            one_post.verify_like = False

        like_posts_pag.append(one_post)

    paginator = Paginator(like_posts_pag,10)
    page = request.GET.get('page')
    
    all_posts_pag = paginator.get_page(page)
    
    return render(request, "network/profile.html", {"all_posts":all_posts_pag,"user_prof":user_prof,"follows":follow_count,"followed":followed_count, "relation":relation})


def follow_to(request,id):
    user_query = User.objects.get(pk=id)
    relation = Followers.objects.create(user=user_query , follower=request.user)
    relation.save()

    return show_user(request, id)
    

def following_to(request, id):
    user_profile = User.objects.get(pk=id)
    
    flag=True
    posts=None
    try:
        followed_counts = Followers.objects.filter(follower=user_profile)
        for user_follow in followed_counts:
            print(user_follow.user)
            try:
                if flag==True:
                    print("Entro al primer if")
                    posts = Post.objects.filter(user=user_follow.user).order_by('-date')
                    flag = False 
                   
                else:
                    posts |= Post.objects.filter(user=user_follow.user).order_by('-date')
            except:
                print("No existen publicaciones")
                posts = None   
                pass 
    except:
        
        print("No sigue a ninguna cuenta aun") 

    #Verificar likes y paginacion
    like_posts=[]
    if posts != None:
        for one_post in posts:
            try:
                like = Like.objects.filter(user=request.user, post=one_post) 
            except:
                like=None
                print("Error al obtener like")

            if like:
                one_post.verify_like = True
            else:
                one_post.verify_like = False

            like_posts.append(one_post)

        paginator = Paginator(like_posts,10)
        page = request.GET.get('page')
        
        all_posts = paginator.get_page(page)
    else:
        all_posts=[]

    return render(request, "network/following.html", {"all_posts":all_posts,"user_prof":user_profile})


def update_post(request):
    
    if request.method == "POST":
        print(f"la request es: ", request.POST['id'] )
        post =  Post.objects.get(pk = request.POST['id'])
        post.text=request.POST['text']
        post.save()
        print("post update")

    return redirect('')


def add_like(request):
    
    if request.method == "POST":
        print(f"el like lo dio el usuario ", request.user)
        post_like= Post.objects.get(pk=request.POST["id"])
        
        new_like = Like.objects.create(user=request.user,post = post_like)
        new_like.save()
        print("Like creado")

        post_like.likes = Like.objects.filter(post=request.POST["id"]).count()
        post_like.save()
        print("Like guardado en post")

def remove_like(request):

    if request.method == "POST":
        post_like= Post.objects.get(pk=request.POST["id"])

        like = Like.objects.filter(user=request.user, post=post_like)
        like.delete()
        print("Like eliminado")

        post_like.likes = Like.objects.filter(post=request.POST["id"]).count()
        post_like.save()
        print("Like guardado en post")

def unfollow_to(request, id):
    user_query = User.objects.get(pk=id)
    relation = Followers.objects.filter(user=user_query , follower=request.user)
    relation.delete()

    return show_user(request, id)
    










    # try:
    #     follows = Followers.objects.get(user=user_prof)
    # except:
    #     follows=None
    #     print(f"El valor de follows es : ",follows)

    # all_posts = Post.objects.get(user=user_prof)
    # all_p = []

    # try:
    #     print(len(all_posts))
    # except (TypeError):
    #     all_p.append(Post.objects.get(user=user_prof))
    #     all_posts = all_p