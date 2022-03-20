from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from musiclib.models import Artist, Album, Playlist, Song
import os
from pathlib import PurePath
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



def songs_by_dir(request):

    songs = Song.objects.all();

    songs_paths = [song.song_file.path for song in songs];

    common_root = os.path.commonpath(songs_paths);

    tracks_tree = { common_root : {} }

    for song in songs:
        song_path = song.song_file.path

        #song_dir = os.path.dirname(song_path)

        relative_path = os.path.relpath(song_path, common_root)
        dir_path, file_name = os.path.split(relative_path)

        parts = PurePath(dir_path).parts

        current = tracks_tree[common_root]
        for dir_name in parts:
            cur_dir = current.get(dir_name)
            if cur_dir:
                current = cur_dir 
            else:
                current[dir_name] = {}
                current = current[dir_name]


        artist_name = song.artist.name if song.artist != None else None
        album_name = song.album.name if song.album != None else None

        current[file_name] = { "file_name": file_name, "track_url" : song.song_file.url, "track_name" : song.name, "album" : album_name, "artist" : artist_name } # Leaf

    return JsonResponse(tracks_tree)
                




'''
def songs_by_artist(request, artist):
    songs = Song.objects.filter(artist__name = artist.name);

    context = {
            "songs" : songs,
    };
'''

