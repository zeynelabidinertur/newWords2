# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from music.models import MyUser
from music.models import Album, Song


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo', 'public']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'song_youtube_url']



