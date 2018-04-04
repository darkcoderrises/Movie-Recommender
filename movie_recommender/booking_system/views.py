from .models import *
from .serializers import CrewSerializer, CrewProfile, MovieSerializer, Movie, Crew
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render
from .filters import UserFilter
from .forms import UpdateProfile, CustomUserCreationForm
from functors.booker import Booker
from functors.recommender import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from datetime import date

# Create your views here.


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


def render_with_user(request, template_name, args):
    args['user'] = request.user
    return render(request, template_name, args)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user.save()
            user_profile = UserProfile.objects.create(user=user, gender=Gender.objects.all()[0])
            user_profile.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render_with_user(request, 'signup.html', {'form': form})


def signup_theaterowner(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            my_group = Group.objects.get(name='TheaterOwnerGroup')
            my_group.user_set.add(user)
            user.is_staff = True
            user.save()
            user_profile = UserProfile.objects.create(user=user, gender=Gender.objects.all()[0])
            user_profile.save()
            return HttpResponseRedirect("/admin/")
    else:
        form = CustomUserCreationForm()
        form.helper.form_action = "/theater_owner/signup"
    return render_with_user(request, 'theater_owner_signup.html', {'form': form})


def search(request):
    movie_list = Movie.objects.all()
    movie_filter = UserFilter(request.GET, queryset=movie_list)
    return render_with_user(request, 'movie_list.html', {'filter': movie_filter})


def get_booking_details(book_obj):
    review = Review.objects.filter(user=book_obj.user, movie=book_obj.show.movie).last()
    if review is None:
        return {'booking': book_obj, 'review': {'rating': 0}}
    else:
        return {'booking': book_obj, 'review': review}


@login_required
def rate(request, movie_id):
    user = request.user
    movie = Movie.objects.get(pk=movie_id)
    rating = request.GET.get('rating')

    review, create = Review.objects.get_or_create(user=user, movie=movie)
    review.rating = rating
    review.save()

    return JsonResponse({})


@login_required
def booking(request):
    bookings = Booking.objects.filter(user=request.user)
    booking_views = [render_to_string('booking_card.html',
                                      get_booking_details(book_obj)) for book_obj in bookings]
    return render_with_user(request, 'bookings.html', {'bookings': booking_views})


@login_required
def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('index')
    else:
        form = UpdateProfile()
        #TODO base values

    args['form'] = form
    args['user'] = request.user
    return render(request, 'update_profile.html', args)


def user_home(request):
    movies = Movie.objects.all()[:4]
    movie_views = [render_to_string('movie_thumbnail.html', {'movie': movie}) for movie in movies]
    return render_with_user(request, 'user_home.html', {'movies': movie_views})


def home(request):
    if request.user.is_authenticated:
        return user_home(request)

    # Setup things for home.
    from functors.recommender import PopularRecommender
    PR = PopularRecommender()
    worldwide = PR.top(10)
    city_id = request.GET.get('city', '')
    city = []
    if city_id:
        city = PR.top_by_city(city_id, 10)

    return render(request, 'home.html', {'worldwide': worldwide, 'city':
        city})


def show_movies(request):
    movies = Movie.objects.all()
    return render_with_user(request, 'movies.html', {'movies': movies})


def show_cast(request):
    if request.method == "POST":
        return HttpResponse("Only supports GET request")

    _crew = CrewProfile.objects.all()
    return render_with_user(request, 'cast.html', {'crews': _crew})


def running(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def upcoming(request):
    # movies = Movie.objects.filter(release_date__gte=date.today())
    movies = Movie.objects.filter(release_date__gte=date(1995, 4, 1)) #testing
    # print(movies)
    return render_with_user(request, 'movies.html', {'movies': movies})


def payment(request):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def book_show(request, show_id):
    booker = Booker()
    show = Show.objects.get(pk=show_id)
    seats = booker.retrieve(show)
    num_rows = len(set([i.row_id for i in seats]))
    num_cols = len(set([i.col_id for i in seats]))
    matrix = [[{"selected": True} for i in range(num_rows)] for i in range(num_cols)]

    for seat in seats:
        row_id = ord(seat.row_id) - ord('A')
        col_id = int(seat.col_id) - 1
        matrix[col_id][row_id] = {
            "selected": False,
            "id": seat.id,
        }

    return render_with_user(request, "book_show.html", {
        'show': show,
        'movie': show.movie,
        'matrix': matrix,
        })


def start_booking(request, show_id):
    show = Show.objects.get(pk=show_id)
    user = request.user.userprofile
    booker = Booker()
    booking = booker.start_booking(show, user)
    return JsonResponse({"booking": model_to_dict(booking)})


def cancel_booking(request, booking_id):
    user = request.user.userprofile
    booking = Booking.objects.get(pk=booking_id)
    if booking.user != user:
        return JsonResponse({"success": False})
    booker = Booker()
    booker.cancel(booking)
    return JsonResponse({})


def add_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    Booker.select(booking_id, seat_id, request.user.userprofile.id)
    return JsonResponse({})


def delete_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    Booker.deselect(booking_id, seat_id, request.user.userprofile.id)
    return JsonResponse({})


def proceed(request):
    booking_id = request.GET.get("booking_id")
    if Booking.objects.filter(pk=booking_id).count():
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def movie(request, movie_id):
    try:
        _movie = Movie.objects.get(pk=movie_id)
        return render_with_user(request, 'movie.html', {"movie": _movie})
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>Movie Does not exist</h1>')


def confirm_booking(request, show_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def crew(request, crew_id):
    try:
        _crew = CrewProfile.objects.get(pk=crew_id)
        _crew_type = Crew.objects.get(profile=crew_id)
        _movies = Movie.objects.filter(crew=_crew_type.id)
        return render_with_user(request, 'crew_profile.html', {"crew": _crew, "crew_type" : _crew_type, "movies": _movies})
    except CrewProfile.DoesNotExist:
        return HttpResponseNotFound('<h1>Crew profile Does not exist</h1>')


def theater(request, theater_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def popular(request):
    recommender = PopularRecommender()
    ordered = recommender.top(5)
    # print(ordered)
    return render_with_user(request, 'popular.html', {"popular": ordered})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')


def similar(request, movie_id):
    query = Movie.objects.get(id=movie_id)
    recommender = CBRecommender()
    ordered = recommender.top(query)
    return render_with_user(request, 'popular.html', {"popular": ordered})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')


def popular_by_genre(request, genre):
    recommender = PopularRecommender()
    ordered = recommender.top_by_genre(genre, 5)
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def shows(request, movie_id):
    # _shows = Show.objects.filter(movie=movie_id)
    movie = Movie.objects.get(pk=movie_id)
    theater_wise = {}
    for show in movie.show_set.all():
        theater_show = show.screen.theater
        theater_wise[theater_show] = theater_wise.get(theater_show, set())
        theater_wise[theater_show].add(show.show_time.strftime("%H:%S"))

    for theater, timings in theater_wise.items():
        theater_wise[theater] = sorted(timings)
    # print (theater_wise)

    return render_with_user(request, 'shows.html', {"movie": movie,"timings": theater_wise})


def review(request, movie_id):
    reviews = Review.objects.filter(movie=movie_id)
    return render_with_user(request, 'review.html', {"reviews": reviews})
