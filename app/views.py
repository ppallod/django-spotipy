from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from .models import User, Song
from .utils import SpotifyAPI
from decouple import config
import os
import json

# SpotifyAPI Authorization
client_id = config("client_id")
client_secret = config("client_secret")
spotify = SpotifyAPI(client_id,client_secret)
spotify.perform_auth()


def index(request):
    
    if request.method == 'GET':
        return render(request,"app/index.html")
    
    elif request.method == 'POST':
        query = request.POST["query"]
        entity = request.POST["entity"]

        #Allowed Entities are album, artist, track

        if spotify.authenticated == False:
            spotify.perform_auth()
        
        response = spotify.search(query=query, entity=entity)
        request.session[f'{entity}'] = response
        return HttpResponseRedirect(reverse(f'{entity}'))

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
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


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
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")

def album(request):
    data = request.session['album']
    items = data["albums"]["items"]
    page_obj = Paginator(items, 5)

    try:
        page = int(request.GET['page'])
    except:
        page = 1
    
    return render(request,"app/album.html", {
        'albums': page_obj.page(page),
        'page_obj':page_obj.page(page),
        'has_next': page_obj.page(page).has_next(),
        'has_previous': page_obj.page(page).has_previous(),
        'request': request
    })

    

def artist(request):
    data = request.session['artist']    
    items = data["artists"]["items"]
    page_obj = Paginator(items, 5)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    return render(request,"app/artist.html", {
        'artists': page_obj.page(page),
        'page_obj':page_obj.page(page),
        'has_next': page_obj.page(page).has_next(),
        'has_previous': page_obj.page(page).has_previous(),
        'request': request
    })


def track(request):
    return HttpResponse("Inside track") 

def oneartist(request, id):
    artist = spotify.get_artist(id, entity='')
    albums = spotify.get_artist(id, entity='albums')
    tracks = spotify.get_artist(id, entity='top-tracks')['tracks']
    
    with open('data_oneartist_toptracks.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)        

    return render(request, "app/artistdetails.html", {
        "artist": artist,
        "albums": albums,
        "tracks": tracks
    })

def onealbum(request, id):
    album = spotify.get_album(id, entity='')
    #with open('data_onealbum.json', 'w', encoding='utf-8') as f:
    #    json.dump(album, f, ensure_ascii=False, indent=4)

    tracks = spotify.get_album(id, entity='tracks')['items']
    with open('data_onealbum_tracks.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)
        
    return render(request, "app/albumdetails.html", {
        "album": album,
        "tracks": tracks
    })

def profile(request, id):
    
    requesting_user = request.user
    id = int(id)
    profile = User.objects.get(pk=id)

    if profile is None:
        return HttpResponse("Profile does not exists")
    
    else:
        tracks = Song.objects.filter(user=profile).order_by('-timestamp').all()
        return render(request, "app/profile.html", {
            'profile': profile,
            'tracks': tracks
        })

def addsong(request):
    if request.method == "GET":
        return JsonResponse({'error': 'request method not allowed'})
    
    elif request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        flag = data.get("flag")
        song_id = data.get("song_id")
        name = data.get("name")
        artist = data.get("artist")
        image_url = data.get("image_url")
        preview_url = data.get("preview_url")
        print(flag)

        if flag=="add":
            Song(user=user, song_id=song_id, name=name, artist=artist, preview_url=preview_url,image_url=image_url).save()
            print("songadded")
        else:
            Song.objects.filter(user=user, song_id=song_id).delete()

        return JsonResponse({'success': 'song added'})