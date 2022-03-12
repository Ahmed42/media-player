from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from musiclib.models import Artist, Album, Playlist, Song
import os
# Create your views here.

def index(request):
    return HttpResponse("Hehe musiclib index!");


def playback(request):
    artists = Artist.objects.all();
    albums = Artist.objects.all();
    playlists = Playlist.objects.all();

    songs_dict = dict();

    songs = Song.objects.all();

    for song in songs:
        artist = song.artist;
        album = song.album;

        # This is an ugly hack ..
        artist = Artist(id=-1, name="Unknown Artist") if not artist else artist;
        album = Album(id=-1, name="Unknown Album") if not album else album;

        if songs_dict.get(artist):
            if songs_dict.get(artist).get(album):
                songs_dict[artist][album].append(song)
            else:
                songs_dict[artist][album] = [song];
        else:
            albums_dict = {album: [song]};
            songs_dict[artist] = albums_dict;


    #songs = Song.objects.filter(artist=None).filter(album=None);

    context = {
            #"artists": artists,
            #"playlists": playlists,
            "songs_dict": songs_dict,
    };

    return render(request, "musiclib/playback.html", context);

def artists(request):
    artists = Artist.objects.all();


'''
def songs_by_artist(request, artist):
    songs = Song.objects.filter(artist__name = artist.name);

    context = {
            "songs" : songs,
    };
'''

