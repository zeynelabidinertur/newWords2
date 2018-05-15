# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from musicweb import settings

fileStorage = FileSystemStorage(location=settings.MEDIA_ROOT)


class Bookshelf(models.Model):
    bookshelf_label = models.CharField(max_length=500)
    description = models.CharField(max_length=100, blank=True, null=True)
    bookshelf_logo = models.FileField(storage=fileStorage, blank=True, null=True)
    public = models.BooleanField(default=False)
    clicks = models.IntegerField(default=0)

    # def get_absolute_url(self):
    #     return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.bookshelf_label


class Book(models.Model):
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=250)
    book_cover = models.FileField(storage=fileStorage, blank=True, null=True)
    author = models.CharField(max_length=250)
    mp3_file = models.FileField(storage=fileStorage, blank=True, null=True)
    doc_file = models.FileField(storage=fileStorage, blank=True, null=True)
    pdf_file = models.FileField(storage=fileStorage, blank=True, null=True)
    txt_file = models.FileField(storage=fileStorage, blank=True, null=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.book_title


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100, blank=True, null=True)
    album_logo = models.FileField(storage=fileStorage, blank=True, null=True)
    public = models.BooleanField(default=False)
    clicks = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + " - " + self.artist


class MyUser(AbstractUser):
    bookshelfs = models.ManyToManyField(Bookshelf, blank=True, null=True)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    song_youtube_url = models.CharField(max_length=1000, blank=True, null=True)
    video_file = models.FileField(storage=fileStorage, blank=True, null=True)
    audio_file = models.FileField(storage=fileStorage, blank=True, null=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.song_title

