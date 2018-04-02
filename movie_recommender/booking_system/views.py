from rest_framework import generics
from .serializers import CrewSerializer, CrewProfile, MovieSerializer, Movie, Crew
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core import serializers
import json
#from booking_system.models import Genre
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import UserFilter
#import django_filters
from itertools import chain
from .forms import UserProfileCreationForm,TheaterOwnerCreationForm,UpdateProfile
#from .forms import LoginForm
from django.core.exceptions import ViewDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# Create your views here.


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


# class CastList(generics.ListCreateAPIView):
#     queryset = Cast.objects.all()
#     serializer_class = CastSerializer
# 
# 
# class CastDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cast.objects.all()
#     serializer_class = CastSerializer
# 
# 
# class MovieList(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer


#class LoginView(FormView):
#    success_url = reverse_lazy('home')
#    template_name = 'login.html'
#
#    def form_valid(self, form):
#        username = form.cleaned_data['username']
#        user = authenticate(username=username, password=password)

#        if user is not None and user.is_active:
#            login(self.request, user)
#            return super(LoginView, self).form_valid(form)
#            return self.form_invalid(form)

#def login(request):
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('index')
#    else:
#        form = LoginForm()
#    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserProfileCreationForm()
    return render(request, 'signup.html', {'form': form})

def signup_theaterowner(request):
    if request.method == 'POST':
        form = TheaterOwnerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = TheaterOwnerCreationForm()
    return render(request, 'signup_theaterowner.html', {'form': form})

def search(request):
    movie_list = Movie.objects.all()
    #for movie in movie_list:
     #   print("<{}>".format(movie.title))
    #print(movie_list)
    movie_filter = UserFilter(request.GET, queryset=movie_list)
    #print(movie_filter.qs)
    return render(request, 'movie_list.html', {'filter': movie_filter})


@login_required
def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse('update_profile_success'))
            return redirect('index')
    else:
        form = UpdateProfile()

    args['form'] = form
    return render(request, 'update_profile.html', args)


def show_movies(request):
    movies = Movie.objects.all()
    #movie_list = [render_to_string("movie_thumbnail.html", MovieSerializer(movie).data) for movie in queryset]
    return render(request, 'movies.html', {'movies': movies})


def show_cast(request):
    if request.method == "POST":
        return HttpResponse("Only supports GET request")

    _crew = CrewProfile.objects.all()
    return render(request, 'cast.html', {'crews': _crew})
    # cast = CrewProfile.objects.get(id=cast_id)
    # cast_data = CrewSerializer(cast)

    # movie_list = cast.movie_set.all()
    # movie_list = [render_to_string("movie_thumbnail.html", MovieSerializer(movie).data) for movie in movie_list]

    # return render(request, 'cast.html', {"cast": cast_data.data, "movies": movie_list})

def running(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def upcoming(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def payment(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def book_show(request, show_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def movie(request, movie_id):
    # print(movie_id, type(movie_id))
    try:
        _movie = Movie.objects.get(pk=movie_id)
        return render(request, 'movie.html', {"movie": _movie})
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>Movie Does not exist</h1>')

def confirm_booking(request, show_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def crew(request, crew_id):
    try:
        _crew = CrewProfile.objects.get(pk=crew_id)
        _crew_type = Crew.objects.get(profile=crew_id)
        _movies = Movie.objects.get(crew=_crew_type.id)
        return render(request, 'crew_profile.html', {"crew": _crew, "crew_type" : _crew_type, "movies": _movies})
    except CrewProfile.DoesNotExist:
        return HttpResponseNotFound('<h1>Crew profile Does not exist</h1>')

def theater(request, theater_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')
