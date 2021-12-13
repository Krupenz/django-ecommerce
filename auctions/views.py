from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Watchlist, AuctionListing
from auctions import models
import datetime

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = models.AuctionListing
        fields = ['name', 'image', 'description', 'category']


class BidForm(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['amount']


def index(request):
    return render(request, "auctions/index.html", {
        "listings": models.AuctionListing.objects.all()
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


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        form_bid = BidForm(request.POST)
        if form.is_valid() and form_bid.is_valid():
            new_listing = models.AuctionListing(
                name=form.cleaned_data['name'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                owner=request.user,
                category=form.cleaned_data['category']
            )
            new_bid = models.Bid(
                auction_listing=new_listing,
                amount=form_bid.cleaned_data['amount'],
                date=datetime.datetime.now()
            )
            new_listing.save()
            new_bid.save()
    form = AuctionListingForm()
    form_bid = BidForm()
    return render(request, "auctions/create.html", {
        "form": form,
        "form_bid": form_bid
    })


def listing(request, id):
    #check if user has it on watchlist
    try:
        auction_listing_id = AuctionListing.objects.get(id=id)
        Watchlist.objects.get(owner=request.user, auction_listing=auction_listing_id)
        on_watchlist = True
    except Watchlist.DoesNotExist:
        on_watchlist = False
    return render(request, "auctions/listing.html", {
        "listing": models.AuctionListing.objects.get(id=id),
        "on_watchlist": on_watchlist
    })


@login_required(login_url='/login')
def add_to_watchlist(request, id):
    if request.method == "POST":
        try:
            auction_listing_id = AuctionListing.objects.get(id=id)
            Watchlist.objects.get(owner=request.user, auction_listing=auction_listing_id)
        except Watchlist.DoesNotExist:
            watchlist_obj = Watchlist.objects.create(owner=request.user, auction_listing=auction_listing_id)
            watchlist_obj.save()
    return HttpResponseRedirect(reverse("listing",args=[id]))

@login_required(login_url='/login')
def remove_from_watchlist(request, id):
    if request.method == "POST":
        try:
            auction_listing_id = AuctionListing.objects.get(id=id)
            watchlist_obj = Watchlist.objects.get(owner=request.user, auction_listing=auction_listing_id)
            watchlist_obj.delete()
        except Watchlist.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse("listing",args=[id]))