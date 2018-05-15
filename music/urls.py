# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'albums/$', views.show_albums, name="albums"),
    url(r'albums/(?P<album_id>[0-9]+)/$', views.show_song_set, name="song-set"),
    url(r'albums/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/$', views.albums_play_song, name="albums-play-song"),
    url(r'album/add/$', views.create_bookshelf, name="bookshelf-create"),
    url(r'^album/(?P<album_id>[0-9]+)/$', views.user_album_detail, name="user-album-detail"),
    url(r'album/(?P<album_id>[0-9]+)/delete/$', views.delete_album, name="album-delete"),
    url(r'^album/(?P<album_id>[0-9]+)/select$', views.select_song, name="song-select"),
    url(r'album/(?P<album_id>[0-9]+)/song/delete/$', views.delete_song, name="song-delete"),
    url(r'album/(?P<album_id>[0-9]+)/update/$', views.update_album, name="album-update"),
    url(r'user/(?P<user_id>[0-9]+)/$', views.user_index_view, name="user-index"),
    url(r'album/(?P<album_id>[0-9]+)/add-song/$', views.upload_song, name="song-upload"),
    url(r'album/(?P<album_id>[0-9]+)/add-song-1/$', views.albums_add_mode, name="albums-add-mode"),
    # url(r'album/(?P<album_id>[0-9]+)/add-song-1/(?P<add_album_id>[0-9]+)/$',
    #     views.albums_song_set_add_mode, name="albums-song-set-add-mode"),
    # url(r'album/(?P<album_id>[0-9]+)/add-song-1/(?P<add_album_id>[0-9]+)/(?P<add_song_id>[0-9]+)/$',
    #     views.albums_play_song_add_mode, name="albums-play-song-add-mode"),
    url(r'album/(?P<album_id>[0-9]+)/songs_added/$', views.song_add_albums, name="song-add"),
    url(r'album/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/$', views.play_song, name="play-song"),
    url(r'album/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/video-upload/$', views.upload_video, name="video-upload"),
    url(r'album/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/audio-upload/$', views.upload_audio, name="audio-upload"),
    url(r'album/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/youtube-embed/$', views.embed_youtube, name="youtube-embed"),
    url(r'^practice/$', views.try_it, name="try-it"),
    url(r'^', views.wrong_url, name='wrong-url')
]

