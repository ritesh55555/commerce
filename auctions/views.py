from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User , Listing , Watchlist 


def index(request):
    if request.method == "POST" :
        listing = Listing(title=request.POST['title'] , details=request.POST['details'] , price=int(request.POST['price']) , owner=request.user.username ,buyer ="none")
        listing.save()

    id_list = []
    for i in Watchlist.objects.filter(name= request.user.username) :
        id_list.append(i.item)
    return render(request, "auctions/index.html" , {
        "listings": Listing.objects.all() ,
        "check" : id_list
    })

def create(request) :
    return render(request , "auctions/create.html")

def bid(request , listing_id ):
    listing = Listing.objects.get(id=listing_id)

    if request.method == "POST" :
        if 'remove' in request.POST :
            listing.delete()
            return render (request , "auctions/index.html" , {
                "listings" : Listing.objects.all()
            })
        
        if 'bid' in request.POST :
            if int(request.POST['price']) > listing.price :
                listing.price = int(request.POST.get('price' , False))
                listing.buyer = request.user.username 
                listing.save()  

        if 'add' in request.POST :
            watchlist = Watchlist(name = request.user.username , item = listing_id)
            watchlist.save()
            return HttpResponseRedirect(reverse(index))

        if 'rw' in request.POST :
            for i in Watchlist.objects.all() :
                if request.user.username == i.name and i.item == listing_id :
                    watchlist = i
            watchlist.delete()
            return HttpResponseRedirect(reverse(index))

    print(listing.price)
    return render (request , "auctions/bid.html" , {
        "listing" : listing
    })

def watchlist(request):
    list = [] 
    for watchlist in Watchlist.objects.all() :
        if request.user.username == watchlist.name :
            list.append(Listing.objects.get(id=watchlist.item))

    return render(request , "auctions/watchlist.html" , {
        "listings" : list
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
