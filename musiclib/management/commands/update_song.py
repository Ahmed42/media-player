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
    def add_song(self, filename, seconds):
        # TODO add code to preprocess song file for metadata (song name, artist, album, genre maybe?)
        #with open(os.path.join(settings.MEDIA_ROOT, filename), 'rb') as f:
            #songf = File(f, name=filename)

        song_metadata = mutagen.File(os.path.join(settings.MEDIA_ROOT, filename))

        new_song = Song(song_file=filename, time_added=seconds)
        
       
        new_song.name = song_metadata.get('title', [None])[0]

        date = song_metadata.get('date', [None])[0] 

        artist_name = song_metadata.get('artist', [None])[0]

        if artist_name:
            try:
                artist = Artist.objects.get(name=artist_name)
            except Artist.DoesNotExist:
                artist = Artist(name=artist_name)
                artist.save()

            new_song.artist = artist

        album_name = song_metadata.get('album')

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
        song_to_delete.delete()


    def add_arguments(self, parser):
        parser.add_argument('event')
        parser.add_argument('seconds', type=int)
        parser.add_argument('filename')

    def handle(self, *args, **options): 
        event = options['event'] 
        seconds = options['seconds'] 
        filename = options['filename'] 

        print("From update_song.py:", event, seconds, filename, sep=' ')

        if((event == 'MOVED_FROM') | (event == 'DELETE')):
            self.remove_song(filename)
        elif((event == 'CREATE') | (event == 'MOVED_TO')):
            self.add_song(filename, seconds)


