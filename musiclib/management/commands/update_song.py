import sys
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from musiclib.models import Song, Artist, Album

import mutagen

'''
This command is to be called by the inotify script whenever a song is added or deleted in the audio dir. It updates the database accordingly. 
'''
class Command(BaseCommand):
    def add_song(self, fullpath, filename, seconds):
        # TODO add code to preprocess song file for metadata (song name, artist, album, genre maybe?)
        #with open(os.path.join(settings.MEDIA_ROOT, filename), 'rb') as f:
            #songf = File(f, name=filename)

        root_path = settings.MEDIA_ROOT

        song_fullname = os.path.join(fullpath, filename)
        song_relativename = song_fullname[len(root_path):].lstrip('/')
        print("Relative name: ", song_relativename)
        song_metadata = mutagen.File(song_fullname)
        

        all_songs = Song.objects.all()
        new_song = None
        for song in all_songs:
            if song.song_file.path == song_fullname:
                # if song already exists, update its metadata instead of creating new entry in DB
                new_song = song
                break

        if not new_song:
            new_song = Song(song_file=song_relativename, time_added=seconds)
        
        if song_metadata:
            new_song.name = song_metadata.get('title', [None])[0]
            date = song_metadata.get('date', [None])[0] 
            artist_name = song_metadata.get('artist', [None])[0]
            album_name = song_metadata.get('album', [None])[0]
        else:
            new_song.name = date = artist_name = album_name = None

        if artist_name:
            try:
                artist = Artist.objects.get(name=artist_name)
            except Artist.DoesNotExist:
                artist = Artist(name=artist_name)
                artist.save()

            new_song.artist = artist



        if album_name:
            try:
                album = Album.objects.get(name=album_name)
            except Album.DoesNotExist:
                album = Album(name=album_name) #, release_date=date)
                album.save()

            new_song.album = album
        

        new_song.save()

    def remove_song(self, filename):
        song_to_delete = Song.objects.get(song_file=filename)
        if song_to_delete:
            song_to_delete.delete()

    def remove_songs_rooted_at(self, fulldirname):
        all_songs = Song.objects.all()

        for song in all_songs:
            if song.song_file.path.startswith(fulldirname):
               song.delete()

    def add_arguments(self, parser):
        parser.add_argument('event')
        parser.add_argument('seconds', type=int)
        parser.add_argument('filename')
        parser.add_argument('fullpath')

    def handle(self, *args, **options): 
        events = options['event'].split(",")
        if len(events) > 1:
            event, isdir = events
        else:
            isdir = None
            event = events[0]

        seconds = options['seconds'] 
        filename = options['filename']
        fullpath = options['fullpath']

        print("From update_song.py:", event, isdir, seconds, fullpath, filename, sep='\n', end='\n\n')


        if isdir == 'ISDIR':
            fulldirname = os.path.join(fullpath, filename)
            if(event == 'MOVED_FROM' or event == 'DELETE'):
                self.remove_songs_rooted_at(fulldirname)
                
            elif(event == 'CREATE' or event == 'MOVED_TO'):
                for fullpath, dirs, filenames in os.walk(fulldirname):
                    for fname in filenames:
                        print("Full path: ", fulldirname, "Filename: ", fname, end="\n\n")
                        # TODO check if it's actually an audio file
                        self.add_song(fulldirname, fname, seconds)

        elif((event == 'MOVED_FROM') or (event == 'DELETE')):
            self.remove_song(filename)
        elif((event == 'CREATE') or (event == 'MOVED_TO')):
            self.add_song(fullpath, filename, seconds)


