# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from forms import RegisterForm
from django.core.files.storage import FileSystemStorage
from .models import *


def index_view(request):
    public_albums = Album.objects.order_by('clicks')
    public_albums1 = []
    for album in public_albums:
        if album.public:
            public_albums1.append(album)

    public_songs = Song.objects.order_by('clicks')
    public_songs1 = []
    for song in public_songs:
        if song.album.public:
            public_songs1.append(song)
    context = {'albums': public_albums}
    try:
        context['album'] = public_albums1[-1]
    except:
        pass
    try:
        context['album1'] = public_albums1[-2]
    except:
        pass
    try:
        context['album2'] = public_albums1[-3]
    except:
        pass
    try:
        context['album3'] = public_albums1[-4]
    except:
        pass
    try:
        context['album4'] = public_albums1[-5]
    except:
        pass
    try:
        context['album5'] = public_albums1[-6]
    except:
        pass

    try:
        context['song'] = public_songs1[-1]
    except:
        pass
    try:
        context['song1'] = public_songs1[-2]
    except:
        pass
    try:
        context['song2'] = public_songs1[-3]
    except:
        pass
    try:
        context['song3'] = public_songs1[-4]
    except:
        pass
    try:
        context['song4'] = public_songs1[-5]
    except:
        pass
    try:
        context['song5'] = public_songs1[-6]
    except:
        pass

    return render(request, 'music/index.html', context)


class UserFormView(View):
    form_class = RegisterForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


def show_albums(request):
    context = {}
    albums = Album.objects.filter(public=True).order_by('clicks').reverse()
    if albums:
        context['albums'] = albums
        context['album'] = albums[0]
    if albums[0].song_set.all():
        context['song'] = albums[0].song_set.all()[0]
    return render(request, 'music/albums.html', context)


def show_song_set(request, album_id):
    context = {}
    albums = Album.objects.filter(public=True)
    if albums:
        context['albums'] = albums
    album_set = Album.objects.filter(pk=album_id)
    if album_set:
        context['album'] = album_set[0]
        album_set[0].clicks += 1
        album_set[0].save()
    if album_set[0].song_set.all():
        context['song'] = album_set[0].song_set.all()[0]
    return render(request, 'music/albums.html', context)


def albums_play_song(request, album_id, song_id):
    context = {}
    albums = Album.objects.filter(public=True)
    if albums:
        context['albums'] = albums
    album_set = Album.objects.filter(pk=album_id)
    if album_set:
        context['album'] = album_set[0]
    song_set = Song.objects.filter(pk=song_id)
    if song_set:
        context['song'] = song_set[0]
        song_set[0].clicks += 1
        song_set[0].save()
    return render(request, 'music/albums.html', context)


def create_bookshelf(request):
    if request.method == "POST":
        bookshelf_label = request.POST.get('bookshelf_label', '')
        description = request.POST.get('description', '')
        bookshelf_privacy = request.POST.get('bookshelf_privacy', '')
        try:
            bookshelf_logo = request.FILES['bookshelf_logo']
        except:
            bookshelf_logo = False

        if len(description) == 0 or len(bookshelf_label) == 0:
            return render(request, 'music/bookshelf_form.html', {"not_completed": "not_completed"})

        if len(bookshelf_privacy) == 0:
            bookshelf_privacy = '1'
        if bookshelf_logo:
            fs = FileSystemStorage()
            filename = fs.save(bookshelf_logo.name, bookshelf_logo)
        else:
            filename = '..\media\default_album_logo.jpg'
        current_user = request.user
        bookshelf2 = Bookshelf()
        bookshelf2.bookshelf_logo = filename
        bookshelf1 = current_user.bookshelfs.create(bookshelf_label=bookshelf_label, description=description, bookshelf_logo=filename,
                                                    public=int(bookshelf_privacy))
        bookshelf1.save()
        current_user.save()
        return render(request, 'music/user_index.html', {'all_albums': current_user.bookshelfs.all()})

    else:
        if request.user.is_active:
            return render(request, 'music/bookshelf_form.html')
        else:
            return redirect('music:index')


def create_album(request):
    if request.method == "POST":
        artist = request.POST.get('artist', '')
        album_title = request.POST.get('album_title', '')
        genre = request.POST.get('genre', '')
        album_privacy = request.POST.get('album_privacy', '')
        try:
            album_logo = request.FILES['album_logo']
        except:
            album_logo = False

        if len(artist) == 0 or len(album_title) == 0:
            return render(request, 'music/bookshelf_form.html', {"not_completed": "not_completed"})

        if len(album_privacy) == 0:
            album_privacy = '1'
        if album_logo:
            fs = FileSystemStorage()
            filename = fs.save(album_logo.name, album_logo)
        else:
            filename = '..\media\default_album_logo.jpg'
        current_user = request.user
        album2 = Album()
        album2.album_logo = filename
        album1 = current_user.albums.create(artist=artist, album_title=album_title, genre=genre, album_logo=filename,
                                            public=int(album_privacy))
        album1.save()
        current_user.save()
        return render(request, 'music/user_index.html', {'all_albums': current_user.albums.all()})

    else:
        if request.user.is_active:
            return render(request, 'music/bookshelf_form.html')
        else:
            return redirect('music:index')


def user_album_detail(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:index')

    if album1.public:
        album1.clicks += 1
        album1.save()
        context = {"album": album1}
        if album1.song_set.all():
            context["song"] = album1.song_set.all()[0]
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, "curr_user": True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def delete_album(request, album_id):
    album1 = Album.objects.get(pk=album_id)
    curr_user = request.user
    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            album1.delete()
        return render(request, 'music/user_index.html', {"all_albums": curr_user.albums.all()})
    return redirect('music:index')


def select_song(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
                context["selected"] = True
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
                context["selected"] = True
            return render(request, 'music/user_index_detail.html', context)

        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def delete_song(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if curr_user.is_active and album1 in curr_user.albums.all():
        if request.method == "POST":

            for key, value in request.POST.items():
                try:
                    song1 = Song.objects.get(pk=int(value))
                    song1.delete()

                except:
                    continue

                """
                if key == 'song' + str(value):
                    song1.delete()
                    break
                elif key == 'song' + str(value) + '-video':
                    song1.video_file = None
                elif key == 'song' + str(value) + '-audio':
                    song1.audio_file = None
                elif key == 'song' + str(value) + '-youtube':
                    song1.song_youtube_url = None
                song1.save()"""

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)

        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def update_album(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if curr_user.is_active and album1 in curr_user.albums.all():
        if request.method == "POST":
            artist = request.POST.get('artist', '')
            album_title = request.POST.get('album_title', '')
            genre = request.POST.get('genre', '')
            album_privacy = request.POST.get('album_privacy', '')

            if len(artist) != 0:
                album1.artist = artist
            if len(album_title) != 0:
                album1.album_title = album_title
            if len(genre) != 0:
                album1.genre = genre
            if len(album_privacy) != 0:
                album1.public = int(album_privacy)
            try:
                album_logo = request.FILES['album_logo']
                fs = FileSystemStorage()
                filename = fs.save(album_logo.name, album_logo)
                album1.album_logo = filename
            except:
                pass

            album1.save()
            current_user = request.user
            user_albums = []
            for album in current_user.albums.all():
                user_albums.append(album)

            return render(request, 'music/user_index.html', {'all_albums': user_albums})

        else:
            if request.user.is_active:
                album = Album.objects.get(pk=album_id)
                if album.public:
                    privacy = 'public'
                else:
                    privacy = 'private'
                return render(request, 'music/album_form_update.html', {"album": album,
                                                                        "privacy": privacy})
            else:
                return redirect('music:user-album-detail')
    if curr_user.is_active:
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def user_index_view(request, user_id):
    curr_user = request.user
    if int(curr_user.id) == int(user_id):
        return render(request, 'music/user_index.html', {"all_albums": curr_user.albums.all()})
    return redirect('music:login')


def upload_song(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if curr_user.is_active and album1 in curr_user.albums.all():
        if request.method == "POST":
            album1 = Album.objects.get(pk=album_id)
            song_title = request.POST.get('song_title', '')
            song_youtube_url = request.POST.get('song_youtube_url', '')
            song_youtube_url = song_youtube_url.split('&')[0]
            song_youtube_url = song_youtube_url.replace("watch?v=", "embed/")
            try:
                video_file = request.FILES['video_file']
            except:
                video_file = None
            try:
                audio_file = request.FILES['audio_file']
            except:
                audio_file = None

            if not song_title:
                return render(request, 'music/song_form.html', {"not_completed": "not_completed",
                                                                "album": album1})
            album1 = Album.objects.get(pk=album_id)
            song_1 = Song()
            song_1.album = album1
            song_1.song_title = song_title
            song_1.song_youtube_url = song_youtube_url
            song_1.video_file = video_file
            song_1.audio_file = audio_file
            song_1.save()
            return render(request, 'music/user_index_detail.html', {"album": album1,
                                                                    'song': song_1,
                                                                    "curr_user": True})

        else:
            if request.user.is_active:
                album1 = Album.objects.get(pk=album_id)
                return render(request, 'music/song_form.html', {"album": album1})
            else:
                return redirect('music:login')

    if curr_user.is_active:
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def albums_add_mode(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if curr_user.is_active and album1 in curr_user.albums.all():
        context = {'album_id': album_id}
        albums = Album.objects.filter(public=True)
        if albums:
            context['albums'] = albums
            context['add_album'] = albums[0]
        if albums[0].song_set.all():
            context['song'] = albums[0].song_set.all()[0]
        return render(request, 'music/albums_add_mode.html', context)

    if curr_user.is_active:
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')

"""
def albums_song_set_add_mode(request, album_id, add_album_id):
    context = {'album_id': album_id}
    albums = Album.objects.filter(public=True)
    if albums:
        context['albums'] = albums
    album_set = Album.objects.filter(pk=add_album_id)
    if album_set:
        context['album'] = album_set[0]
    if album_set[0].song_set.all():
        context['song'] = album_set[0].song_set.all()[0]
    return render(request, 'music/albums_add_mode.html', context)


def albums_play_song_add_mode(request, album_id, add_album_id, add_song_id):
    context = {'album_id': album_id}
    albums = Album.objects.filter(public=True)
    if albums:
        context['albums'] = albums
    album_set = Album.objects.filter(pk=add_album_id)
    if album_set:
        context['album'] = album_set[0]
    song_set = Song.objects.filter(pk=add_song_id)
    if song_set:
        context['song'] = song_set[0]
    return render(request, 'music/albums_add_mode.html', context)
"""


def song_add_albums(request, album_id):
    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if curr_user.is_active and album1 in curr_user.albums.all():
        if request.method == "POST":
            for value in request.POST.getlist('songs'):
                song1 = Song.objects.get(pk=int(value))
                song1 = Song(album=album1, song_title= song1.song_title, song_youtube_url=song1.song_youtube_url,
                             video_file=song1.video_file, audio_file=song1.audio_file, clicks=0)
                song1.save()

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)

        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def play_song(request, album_id, song_id):
    curr_user = request.user
    try:
        song_1 = Song.objects.get(pk=song_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    album1 = song_1.album

    if not album1.public and (curr_user.is_active and album1 not in curr_user.albums.all()):
        return redirect('music:index')
    else:
        song_1.clicks += 1
        song_1.save()
        context = {"album": album1, 'play_song': song_1}

        if curr_user.is_active:
            if album1 in curr_user.albums.all():
                context["curr_user"] = True
        return render(request, 'music/user_index_detail.html', context)


def upload_video(request, album_id, song_id):
    if request.method == 'POST':

        try:
            video_file = request.FILES['video_file']
        except:
            video_file = None
        # fs = FileSystemStorage()
        # filename = fs.save(video_file.name, video_file)
        song_1 = Song.objects.get(pk=song_id)
        song_1.video_file = video_file
        song_1.save()

    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def upload_audio(request, album_id, song_id):
    if request.method == 'POST':
        try:
            audio_file = request.FILES['audio_file']
            song_1 = Song.objects.get(pk=song_id)
            song_1.audio_file = audio_file
            song_1.save()
        except:
            pass

    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def embed_youtube(request, album_id, song_id):
    if request.method == 'POST':
        try:
            song_youtube_url = request.POST.get('youtube_url_embed', '')
            song_youtube_url = song_youtube_url.split('&')[0]
            song_youtube_url = song_youtube_url.replace("watch?v=", "embed/")
            song_1 = Song.objects.get(pk=song_id)
            song_1.song_youtube_url = song_youtube_url
            song_1.save()
        except:
            pass

    curr_user = request.user
    try:
        album1 = Album.objects.get(pk=album_id)
    except:
        if curr_user.is_active:
            return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
        return redirect('music:login')

    if album1.public:
        context = {"album": album1}
        if curr_user.is_active and album1 in curr_user.albums.all():
            context['curr_user'] = True
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
        return render(request, 'music/user_index_detail.html', context)

    if curr_user.is_active:
        if album1 in curr_user.albums.all():
            context = {"album": album1, 'curr_user': True}
            if album1.song_set.all():
                context["song"] = album1.song_set.all()[0]
            return render(request, 'music/user_index_detail.html', context)
        return render(request, 'music/user_index.html', {'all_albums': curr_user.albums.all()})
    return redirect('music:login')


def wrong_url(request):
    return redirect('music:index')


def try_it(request):
    album1 = Album.objects.all()
    return render(request, 'music/try_it.html', {"curr_user": request.user,
                                                 'album1': album1})
