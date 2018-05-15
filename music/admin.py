# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Album, Song, MyUser

admin.site.register(MyUser)
admin.site.register(Album)
admin.site.register(Song)