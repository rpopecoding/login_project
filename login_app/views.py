from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if 'active_user' in request.session:
        user = User.objects.get(id=request.session['active_user'])
        context ={
            "logged_in" : True,
            "user": user
        }
    else:
        context = {
            "logged_in" : False
        }

    print(context)
    
    return render(request, "index.html", context)

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        prehash = request.POST['pwd']   
        
        errors = User.objects.basic_validator(request.POST)
        if request.POST['pwd'] != request.POST['confirm']:
            errors["pwd"] = "Passwords did not match"
        if len(User.objects.filter(email=email)) > 0:
            errors["dupe"] = "Email already in Database"
    
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        posthash = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=email, pwdhash = posthash)
        user = User.objects.last()
        request.session['active_user'] = user.id


    return redirect("/success")
    #request.POST['']

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
       

        user = User.objects.get(email = email)


        check = bcrypt.checkpw(pwd.encode(), user.pwdhash.encode())
        if check == True:
            request.session['active_user'] = user.id
            return redirect("/success")      
        else:
            errors = {}
            errors["pwd"] = "Invalid Password"
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
    return redirect("/")
    

def logout(request):
    request.session.flush()
    return redirect("/")

def success(request):
    if 'active_user' in request.session:
        user = User.objects.get(id=request.session['active_user'])
        context={
            "user": user
            }
        return render(request, "success.html", context)
    return redirect("/")
    
def wall(request):
    if 'active_user' in request.session:
        user = User.objects.get(id=request.session['active_user'])
        all_tweets = Tweet.objects.all()

        context={
            "user": user,
            "all_tweets": all_tweets,
            }
        return render(request, "wall.html", context)
    return redirect("/")

def post_tweet(request):
    if 'active_user' not in request.session:
        return redirect("/")
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        text = request.POST['text']

        errors = Tweet.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        Tweet.objects.create(text=text, author=user)
        return redirect("/wall")
    return redirect('/')

def comment(request):
    if 'active_user' not in request.session:
        return redirect("/")
    if request.method == "POST":

        user = User.objects.get(id=request.session['active_user'])
        tweet = Tweet.objects.get(id=request.POST['tweet_id'])
        text = request.POST['text']

        
        Comment.objects.create(text=text, tweet=tweet, author=user)

        return redirect("/wall")
    return redirect('/')

def delete_tweet(request):
    tweet = Tweet.objects.get(id=request.POST['tweet_id'])
    tweet.delete()
    return redirect("/wall")


    