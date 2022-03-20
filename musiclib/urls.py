from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('playback/', views.playback, name='playback'),
        path('songs_by_dir/', views.songs_by_dir, name='songs_by_dir')
]
