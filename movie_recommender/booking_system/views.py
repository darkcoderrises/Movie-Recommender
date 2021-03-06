from .models import *
from .serializers import CrewProfile, Movie, Crew
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
from collections import namedtuple
from functors.notifier import Notifier
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist#, RelatedObjectDoesNotExist

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
    args['home_url'] = settings.HOME_URL
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
            return redirect('/preferences')
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
    bookings = Booking.objects.filter(user=request.user).order_by('-show__show_time')
    done_views = []
    new_views = []

    for book_obj in bookings:
        if book_obj.show.show_time.date() < date(2018, 4, 2):
            view = render_to_string('booking_card.html', get_booking_details(book_obj))
            done_views.append(view)
        else:
            data = get_booking_details(book_obj)
            data['hide'] = True
            view = render_to_string('booking_card.html', data)
            new_views.append(view)

    return render_with_user(request, 'bookings.html', {'done_views': done_views, 'new_views': new_views})


@login_required
def update_profile(request):
    args = {}

    if request.method == 'POST':
        try:
            form = UpdateProfile(request.POST, instance=request.user.userprofile)
        except ObjectDoesNotExist:
            profile = UserProfile(user=request.user,
                    gender=Gender.objects.all().first())
            form = UpdateProfile(request.POST, instance=profile)
        form.actual_user = request.user
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            form.save_m2m()
            return redirect('index')
    else:
        try:
            form = UpdateProfile(initial=model_to_dict(request.user.userprofile))
        except ObjectDoesNotExist:
            profile = UserProfile(user=request.user,
                    gender=Gender.objects.all().first())
            form = UpdateProfile(initial=model_to_dict(profile))

    args['form'] = form
    args['user'] = request.user
    return render(request, 'update_profile.html', args)


def user_home(request):
    CF = CFRecommender()
    PR = PopularRecommender()
    def user_bookings(user):
        bookings = Booking.objects.filter(user=user)
        movies = []
        for booking in bookings:
            movies.append(booking.show.movie)
        return movies

    CB = CBRecommender()
    similar_movies = []
    for movie in user_bookings(request.user):
        similar = CB.top(movie, 10)
        similar_movies.extend(similar)

    similar_movies = list(set(similar_movies))
    recommended = CF.top(request.user, 10)
    try:
        profile = UserProfile.objects.get(user=request.user)
        prefs = profile.genre_pref.all()
        rows = []
        def convert(dictionary):
            return namedtuple('GenericDict', dictionary.keys())(**dictionary)

        for pref in prefs:
            row = PR.top_by_genre(pref.genre, 3)
            _row = {'name': pref.genre, 'movies': row}
            rows.append(convert(_row))
        return render_with_user(request, 'user_home.html', {'genres': rows,
            'recommended': recommended, 'similar': similar_movies})
    except ObjectDoesNotExist:
        return anonymous_home(request)


def anonymous_home(request):
    from functors.recommender import PopularRecommender
    PR = PopularRecommender()
    worldwide = PR.top(10)
    city_id = request.GET.get('city', '')
    city = []
    if city_id:
        city = PR.top_by_city(city_id, 10)

    return render(request, 'home.html', {'worldwide': worldwide, 'city':
        city})


def home(request):
    if request.user.is_authenticated:
        return user_home(request)

    # Setup things for home.
    return anonymous_home(request)


def show_movies(request):
    movies = Movie.objects.all()
    return render_with_user(request, 'movies.html', {'movies': movies})


def show_cast(request):
    if request.method == "POST":
        return HttpResponse("Only supports GET request")

    _crew = CrewProfile.objects.all()
    return render_with_user(request, 'cast.html', {'crews': _crew})


def running(request):
    from datetime import datetime
    shows = Show.objects.filter(show_time__date=datetime.today())
    movies = set([i.movie for i in shows])
    return render_with_user(request, 'movies.html', {'movies': movies, 'active': 'nearby'})


def upcoming(request):
    # movies = Movie.objects.filter(release_date__gte=date.today())
    movies = Movie.objects.filter(release_date__gte=date(1995, 4, 1)) #testing
    return render_with_user(request, 'movies.html', {'movies': movies, 'active': 'upcoming'})


def dummy_gateway(request):
    amount = request.GET.get('amount', 0)
    id = request.GET.get('id', 0)
    hit_url = request.GET.get('hit_url', settings.HOME_URL + '/payment')

    return render(request, 'dummy_gateway.html', {'amount': amount, 'id': id, 'hit_url': hit_url})


@login_required
def booking_detail(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if booking.user != request.user:
            raise Exception
        review = Review.objects.filter(movie=booking.show.movie, user=booking.user).last()
        rev_data = {'rating': 0}
        if review:
            rev_data = review
        return render(request, 'booking_detail.html', {'booking': booking, 'review': rev_data})
    except Exception as E:
        print(E)
        return redirect('index')


def payment(request):
    booking_id = request.GET.get('id')
    success = request.GET.get('success')
    try:
        booking = Booking.objects.get(id=int(booking_id))
        success = int(success)
        if booking.invoice.status.name != "In Progress":
            return redirect('/booking_detail/' + booking_id)

        booker = Booker()
        if success:
            Notifier().mail(request.user, "Booking Successful", """
                Congratulations, your movie ticket for the movie {0} is successfully booked.
                You can show the following link to see the movie {1}
            """.format(booking.show.movie.title, settings.HOME_URL+'/booking_detail/'+str(booking.id)))
            booker.invoice_success(booking)
        else:
            Notifier().mail(request.user, "Booking Unsuccessful", """
                Sorry the movie ticket you were trying to book was not successful.
            """)
            booker.invoice_failure(booking)

        return redirect('/booking_detail/'+booking_id)

    except Exception as e:
        print(e)
        return redirect('index')


@login_required
def book_show(request, show_id):
    booker = Booker()
    show = Show.objects.get(pk=show_id)
    seats = booker.retrieve(show)
    set_row = list(set([i.row_id for i in seats]))
    set_col = list(set([i.col_id for i in seats]))
    num_rows = len(set_row)
    num_cols = len(set_col)
    matrix = [[{"selected": True} for i in range(num_rows)] for i in range(num_cols)]

    for seat in seats:
        row_id = set_row.index(seat.row_id)
        col_id = set_col.index(seat.col_id)
        matrix[col_id][row_id] = {
            "selected": False,
            "id": seat.id,
            "amount": seat.seat_type.price,
        }

    return render_with_user(request, "book_show.html", {
        'show': show,
        'movie': show.movie,
        'matrix': matrix,
        })


def start_booking(request, show_id):
    show = Show.objects.get(pk=show_id)
    user = request.user
    booker = Booker()
    booking = booker.start_booking(show, user)
    return JsonResponse({"booking": model_to_dict(booking)})


def cancel_booking(request, booking_id):
    user = request.user
    booking = Booking.objects.get(pk=booking_id)
    if booking.user != user:
        return JsonResponse({"success": False})
    booker = Booker()
    booker.cancel(booking)
    return JsonResponse({})


def add_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    Booker.select(booking_id, seat_id, request.user.id)
    return JsonResponse({})


def delete_seat(request, booking_id):
    seat_id = request.GET.get('seat_id')
    Booker.deselect(booking_id, seat_id, request.user.id)
    return JsonResponse({})


def proceed(request):
    booking_id = request.GET.get("booking_id")
    if Booking.objects.filter(pk=booking_id).count():
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def booking_summary(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        return render_with_user(request, "booking_summary.html", {'booking': booking, 'invoice': booking.invoice, 'show': booking.show, 'movie': booking.show.movie})
    except Exception:
        return redirect('index')

def similar_movies(movie_id):
    query = Movie.objects.get(id=movie_id)
    recommender = CBRecommender()
    ordered = recommender.top(query, 5)
    return ordered

def movie(request, movie_id):
    try:
        # def ordered_crew(crew):
        #     d = {}
        #     for c in crew.all():
        #         # val = Movie.objects.values('crew').annotate(count=Count('id')).filter(crew=c)
        #         val = Crew.objects.annotate(movie_count=Count('movie')).order_by('-movie_count').values('movie_count')
        #         print(val)
        #     pass
        #     # Returns crew.

        _movie = Movie.objects.get(pk=movie_id)
        similar_movie = similar_movies(movie_id)
        return render_with_user(request, 'movie.html', {"movie": _movie, 'similar' : similar_movie})
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>Movie Does not exist</h1>')


def confirm_booking(request, show_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')


def crew(request, crew_id):
    try:
        _crew = CrewProfile.objects.get(pk=crew_id)
        _crew_type = Crew.objects.filter(profile=crew_id)
        _movies = Movie.objects.filter(crew=_crew_type[0].id)
        return render_with_user(request, 'crew_profile.html', {"crew": _crew, "crew_type" : _crew_type, "movies": _movies})
    except CrewProfile.DoesNotExist:
        return HttpResponseNotFound('<h1>Crew profile Does not exist</h1>')


def theater(request, theater_id):
    return HttpResponseNotFound('<h1>Page under construction?</h1>')

def similar(request, movie_id):
    query = Movie.objects.get(id=movie_id)
    recommender = CBRecommender()
    ordered = recommender.top(query)
    return render_with_user(request, 'popular.html', {"popular": ordered})
    # return HttpResponseNotFound('<h1>Page under construction?</h1>')

def popular(request):
    recommender = PopularRecommender()
    ordered = recommender.top(5)
    # print(ordered)
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
    dates = set()
    show_to_id = {}

    for show in movie.show_set.all():
        theater_show = show.screen.theater
        theater_wise[theater_show] = theater_wise.get(theater_show, set())
        theater_wise[theater_show].add(show.show_time)
        show_to_id[(theater_show, show.show_time)] = show.id
        dates.add(show.show_time.strftime("%d"))

    dates = sorted(dates)
    final_data = []

    for date in dates:
        data = {'date': date, 'timings': []}

        for theater, timings in theater_wise.items():
            temp = [{
                'time': time.strftime("%H:%M"),
                'id': show_to_id[(theater, time)],
                'date': time.strftime("%d")
            } for time in timings]
            temp = sorted(list(filter(lambda i: i['date'] == date, temp)), key=lambda i: i['time'])
            if len(temp):
                data['timings'].append((theater, temp))
        final_data.append((date, render_to_string('show_timings.html', data)))

    return render_with_user(request, 'shows.html', {"movie": movie, "timings": final_data, "dates": list(dates)})


def review(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = Review.objects.filter(movie=movie_id)
    return render_with_user(request, 'review.html', {"reviews": reviews, "movie": movie})


def user_review(request):
    # print(request.user.id)
    # reviews = Review.objects.filter(user=19)#request.user.id)
    reviews = Review.objects.filter(user=request.user)
    return render_with_user(request, 'user_review.html', {"reviews": reviews})
