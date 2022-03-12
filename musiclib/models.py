from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=50)

class Album(models.Model):
    name = models.CharField(max_length=50)
    #artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.CASCADE)
#    release_date = models.DateTimeField()

class Song(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)
    song_file = models.FileField()
    time_added = models.IntegerField()

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, through='playlistssongs')

class PlaylistsSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    song_position = models.IntegerField()
'''
class Metadata(models.Model):
    pass
'''
