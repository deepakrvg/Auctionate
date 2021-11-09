from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Bids, Comments, WatchList, WinBid

@login_required()
def index(request):
    if request.method == "POST":
        user = request.user
        user_name = user.username
        name = request.POST["name"]
        price = request.POST["price"]
        image = request.POST["image"]
        item_number = request.POST["item_number"]
        try:
            watch = WatchList(name=name, user_name=user_name, price=price, image=image, item_number=item_number)
            watch.save()
        except:
            items = AuctionListing.objects.all()
            return render(request, "auctions/index.html", {
                "items": items
            })
        
        items = AuctionListing.objects.all()
        return render(request, "auctions/index.html", {
            "items": items
        })
    
    else:
        items = AuctionListing.objects.all()
        return render(request, "auctions/index.html", {
            "items": items
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

@login_required()
def create(request):
    if request.method == "POST":
        name = request.POST["name"]
        category = request.POST["category"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]
        description = request.POST["description"]

        if not name:
            return render(request, "auctions/create.html", {
                "message": "Name Required."
            })

        if not price:
            return render(request, "auctions/create.html", {
                "message": "Price Required."
            })
        
        user = request.user
        user_id = user.id

        try:
            item = AuctionListing(name=name, user_id=user_id, category=category, image=image_url, price=price, description=description)
            item.save()
        except:
            return render(request, "auctions/create.html", {
                "message": "Unable to add Auction."
            })
        
        return render(request, "auctions/index.html", {
            "message": "Successfully added Auction."
        })

    else:
        return render(request, "auctions/create.html")

@login_required()
def list(request, number):
    if request.method == "POST":
        bid_price = request.POST["bid_price"]
        user = request.user
        user_id = user.id
        try:
            user_bid = Bids(bid_price=bid_price, user_id=user_id, item_number=number)
            user_bid.save()
        except:
            item = AuctionListing.objects.get(id=number)
            username = User.objects.get(id=item.user_id)
            bids = Bids.objects.filter(item_number=number)
            bids_number = len(bids)
            max_bid = item.price
            for bid in bids:
                if max_bid < bid.bid_price:
                    max_bid = bid.bid_price

            comments = Comments.objects.filter(item_number=number)


            return render(request, "auctions/list.html", {
                "number": number, 
                "item": item,
                "bids_number": bids_number,
                "username": username,
                "user_id": user_id,
                "max_bid": max_bid,
                "message": "Unable to Place Bid.",
                "comments": comments
            })
        
        item = AuctionListing.objects.get(id=number)
        username = User.objects.get(id=item.user_id)
        bids = Bids.objects.filter(item_number=number)
        bids_number = len(bids)
        max_bid = item.price
        for bid in bids:
            if max_bid < bid.bid_price:
                max_bid = bid.bid_price
        
        comments = Comments.objects.filter(item_number=number)

        return render(request, "auctions/list.html", {
            "number": number, 
            "item": item,
            "bids_number": bids_number,
            "username": username,
            "user_id": user_id,
            "max_bid": max_bid,
            "message": "Successfully Placed Bid.",
            "commetns": comments
        })
    
    else:
        user = request.user
        user_id = user.id
        item = AuctionListing.objects.get(id=number)
        username = User.objects.get(id=item.user_id)
        bids = Bids.objects.filter(item_number=number)
        bids_number = len(bids)
        max_bid = item.price
        for bid in bids:
            if max_bid < bid.bid_price:
                max_bid = bid.bid_price

        comments = Comments.objects.filter(item_number=number)

        return render(request, "auctions/list.html", {
            "number": number, 
            "item": item,
            "bids_number": bids_number,
            "username": username,
            "user_id": user_id,
            "max_bid": max_bid, 
            "comments": comments
        })

@login_required()
def comment(request, number):
    if request.method == "POST":
        comment = request.POST["comment"]
        user = request.user
        user_id = user.id
        user_name = user.username
        try:
            user_comment = Comments(comment=comment, item_number=number, user_id=user_id, username=user_name)
            user_comment.save()
        except:
            item = AuctionListing.objects.get(id=number)
            comments = Comments.objects.filter(item_number = number)
            return render(request, "auctions/comment.html", {
                "comments": comments,
                "message": "Unable to add Comment.",
                "item": item
            })

        item = AuctionListing.objects.get(id=number)
        comments = Comments.objects.filter(item_number = number)
        return render(request, "auctions/comment.html", {
            "comments": comments,
            "message": "Comment added Successfully.",
            "item": item
        })
    
    else:
        item = AuctionListing.objects.get(id=number)
        comments = Comments.objects.filter(item_number = number)
        return render(request, "auctions/comment.html", {
            "comments": comments,
            "item": item
        })

@login_required()
def watchlist(request):
    if request.method == "POST":
        id = request.POST["id"]
        item = WatchList.objects.get(pk=id)
        item.delete()
        user_name = request.user.username
        watchs = WatchList.objects.filter(user_name=user_name)
        return render(request, "auctions/watchlist.html", {
            "watchs": watchs,
            "message": "Item removed from watchlist."
        })
    
    else:
        user_name = request.user.username
        watchs = WatchList.objects.filter(user_name=user_name)
        return render(request, "auctions/watchlist.html", {
            "watchs": watchs
        })

@login_required()
def endbid(request):
    if request.method == "POST":
        user_id = request.user.id
        user_name = request.user.username
        item_id = request.POST["item_id"]
        item = AuctionListing.objects.get(pk=item_id)
        bids = Bids.objects.filter(item_number=item_id)
        max_bid = item.price
        for bid in bids:
            if max_bid < bid.bid_price:
                max_bid = bid.bid_price
                winner_id = bid.user_id
                winner_user_name = User.objects.get(pk=winner_id)
        
        user_win_bid = WinBid(item_number=item_id, user_id=winner_id, name=item.name, user_name=winner_user_name, price=max_bid, image=item.image)
        user_win_bid.save()

        bid_item = AuctionListing.objects.get(pk=item_id)
        bid_item.delete()
        items = AuctionListing.objects.all()
        return render(request, "auctions/index.html", {
            "items": items
        })

@login_required()
def history(request):
    user_id = request.user.id
    user_win_bids = WinBid.objects.filter(user_id=user_id)
    return render(request, "auctions/history.html", {
        "user_win_bids": user_win_bids
    })

@login_required()
def categories(request):
    items = AuctionListing.objects.all()
    categories = set()
    for item in items:
        i = item.category
        categories.add(i)

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required()
def category(request, name):
    category_lists = AuctionListing.objects.filter(category=name)
    return render(request, "auctions/category.html", {
        "name": name,
        "category_lists": category_lists
    })
