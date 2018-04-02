from django.core.management.base import BaseCommand
import booking_system.models as M
from datetime import datetime, timedelta
import pandas as pd
import funcy as fy
import random
import numpy


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            help='File path',
        )

    def handle(self, *args, **options):
        self.seed(options['path'])

    # def _seed_cast_type(self):
    #     M.CastType.objects.all().delete()
    #     c = ["Director", "Actor", "Producer"] #Creating three cast types
    #     for i in range(3): 
    #         name = c[i]
    #         _cast_type = M.CastType.objects.create(name=name)
    #         _cast_type.save()

    # def _seed_gender(self):
    #     M.Gender.objects.all().delete()
    #     g = ["Male", "Female"] #Creating two gender
    #     for i in range(2): 
    #         name = g[i]
    #         _gender = M.Gender.objects.create(name=name)
    #         _gender.save()
    
    # def _seed_languages(self, langs):
    #     M.Language.objects.all().delete()
    #     langs = set(list(langs))
    #     for lang in langs:
    #         _lang = M.Language.objects.create(lang=lang)
    #         _lang.save()

    def _seed_status_type(self):
        M.StatusType.objects.all().delete()
        s = ["Success", "Failure", "In Progress"] #Creating three cast types
        for i in range(3):
            name = s[i]
            _status_type = M.StatusType.objects.create(name=name)
            _status_type.save()

    # def _seed_crew_profile(self, crew_profile):
    #     M.CrewProfile.objects.all().delete()
    #     _crew=set()
    #     for i, c in crew_profile.iterrows():
    #         _crew.add(c[0])
    #         _crew.add(c[1])
    #         _crew.add(c[2])
    #         _crew.add(c[3])
    #     g = "Male"
    #     for cp in _crew:
    #         _gender = M.Gender.objects.get(name=g)
    #         _crew_profile = M.CrewProfile.objects.create(name=cp,gender=_gender)
    #         _crew_profile.save()

    # def _seed_genres(self, genres):
    #     M.Genre.objects.all().delete()
    #     transform = lambda x: x.split('|')
    #     genres = list(map(transform, genres))
    #     genres = fy.flatten(genres)
    #     genres = set(genres)
    #     for genre in genres:
    #         _genre = M.Genre.objects.create(genre=genre)
    #         _genre.save()

    # def _seed_user_profile(self):
    #     M.UserProfile.objects.all().delete()
    #     _age = 23
    #     phones = ["0123456789", "1234567890", "2345678901"]#, "3456789012", "4567890123"]
    #     usernames = ['Harshil', 'Jerin', 'Mandar']
    #     passwords = ['Harshil', 'Jerin', 'Mandar']
    #     gen = "Male"
    #     genre_pref = ["Sci-Fi", "Fantasy"]
    #     _genre_pref = [M.Genre.objects.get(genre=g) for g in genre_pref]
    #     _gender = M.Gender.objects.get(name=gen)
    #     #creating 3 users
    #     for i in range(3):
    #         _user_profile = M.UserProfile.objects.create(gender=_gender, age=_age, phone=phones[i], username=usernames[i], password=passwords[i])
    #         _user_profile.genre_pref.set(_genre_pref)
    #         _user_profile.save()

    # def _seed_crew(self, crew):
    #     M.Crew.objects.all().delete()
    #     directors = set()
    #     actors = set()
    #     for i, c in crew.iterrows():
    #         directors.add(c[0])
    #         actors.add(c[1])
    #         actors.add(c[2])
    #         actors.add(c[3])
    #     d = "Director"
    #     a = "Actor"
    #     for director in directors:
    #         _profile = M.CrewProfile.objects.get(name=director)
    #         _role = M.CastType.objects.get(name=d)
    #         _crew = M.Crew.objects.create(profile=_profile, role=_role)
    #         _crew.save()
    #     for actor in actors:
    #         _profile = M.CrewProfile.objects.get(name=actor)
    #         _role = M.CastType.objects.get(name=a)
    #         _crew = M.Crew.objects.create(profile=_profile, role=_role)
    #         _crew.save()

    # def _seed_movies(self, movies):
    #     M.Movie.objects.all().delete()
    #     for i, m in movies.iterrows():
    #         title, lang, genres, crew1, crew2, crew3, crew4 = list(m.values)
    #         genres = genres.split('|')
    #         _lang = M.Language.objects.get(lang=lang)
    #         _movie = M.Movie.objects.create(title=title,
    #                 language=_lang)
    #         #TODO roles of crew
    #         crew = [crew1, crew2, crew3, crew4]
    #         _crew = M.Crew.objects.filter(profile__name__in=crew)
    #         _movie.crew.set(_crew)
    #         _genres = [M.Genre.objects.get(genre=g) for g in genres]
    #         _movie.genres.set(_genres)
    #         _movie.save()

    def _seed_city(self, cities):
        M.City.objects.all().delete()
        city = set(list(cities))
        for c in city:
            _city = M.City.objects.create(name=c)
            _city.save()

    def _seed_location(self, locations):
        M.Location.objects.all().delete()
        for i, l in locations.iterrows():
            name, city, loc_lat, loc_long = list(l.values)
            _city = M.City.objects.get(name=city)
            _location = M.Location.objects.create(name=name, city=_city, location_lat=loc_lat, location_long=loc_long)
            _location.save()

    def _seed_seat_type(self):
        M.SeatType.objects.all().delete()
        s = [('Regular', 200),('Executive', 300)]
        for i in range(2): #Creating two seat types
            name = s[i][0]
            price = s[i][1]
            _seat_type = M.SeatType.objects.create(name=name, price=price)
            _seat_type.save()

    def _seed_theater(self, theatres):
        M.Theater.objects.all().delete()
        for i, t in theatres.iterrows():
            name, loc = list(t.values)
            _loc = M.Location.objects.get(name=loc)
            _theater = M.Theater.objects.create(name=name, location=_loc)
            _theater.save()

    def _seed_screens(self):
        M.Screen.objects.all().delete()
        _theaters=list(M.Theater.objects.all())
        _identifiers=['A','B','C','D', 'E', 'F', 'G', 'H', 'I', 'J']
        for _theater in _theaters:
            mn, mx = 1, 10
            count = random.randint(mn, mx)
            for _identifier in _identifiers[:count]:
                _screen=M.Screen.objects.create(identifier=_identifier, theater=_theater)
                _screen.save()

    def _seed_seat(self):
        M.Seat.objects.all().delete()
        _screens = list(M.Screen.objects.all())
        # _rows = list(map(chr, range(ord('A'), ord('N')+1))) # rows from A - N
        # _columns = list(range(1,11)) # columns from 1 - 10
        _rows = list(map(chr, range(ord('A'), ord('D')+1))) # rows from A - D
        _columns = list(range(1,4)) # columns from 1 - 3
        # A - K "Regular seats"
        for _screen in _screens:
            mn_row, mx_row = 3, 4 # 4, 14
            mn_col, mx_col = 1, 3 # 1, 10
            count_rows = random.randint(mn_row, mx_row)
            count_cols = random.randint(mn_col, mx_col)
            # "Regular Seats"
            for _row in _rows[:(count_rows - 3)]:
                for _column in _columns[: count_cols]:
                    s = "Regular"
                    _seat_type = M.SeatType.objects.get(name=s)
                    _seat = M.Seat.objects.create(screen=_screen,row_id=_row,
                                                  col_id=_column, seat_type=_seat_type)
                    _seat.save()

            # last 3 rows "Executive Seats"
            for _row in _rows[(count_rows - 2) : count_rows]:
                for _column in _columns[:count_cols]:
                    s = "Executive"
                    _seat_type = M.SeatType.objects.get(name=s)
                    _seat = M.Seat.objects.create(screen=_screen,row_id=_row,
                                                  col_id=_column, seat_type=_seat_type)
                    _seat.save()
  
    def _seed_shows(self):
        M.Show.objects.all().delete()
        _screens = list(M.Screen.objects.all())
        _movies = list(M.Movie.objects.all())
        times = [[11,00,14,15,18,00,21,00], 
        [12,00,15,00,19,00,22,00], 
        [11,00,14,00,18,00,21,00]]
        u = datetime.strptime("2018-04-01","%Y-%m-%d")
        l = []
        for i in range(14):# data for two weeks
            d = timedelta(days=i)
            l.append(u + d)
        mn_day, mx_day = 1, 5 
        mn_time, mx_time = 0, 2 
        for _screen in _screens:
            for _movie in _movies:
                count_days = random.randint(mn_day, mx_day)
                time_slot = random.randint(mn_time, mx_time)
                for t in l[:count_days]:
                    for i in range(0, 8, 2):
                        daytime = t.replace(hour=times[time_slot][i], minute=times[time_slot][i + 1])
                        # time = datetime.strptime(_time, '%Y-%m-%d %H:%M:%S').time()
                        _show = M.Show.objects.create(movie=_movie,screen=_screen,
                                                  show_time=daytime)
                        _show.save()

    # def _seed_booking(self):
    #     M.Booking.objects.all().delete()
    #     phones = ["0123456789","1234567890", "2345678901"]#, "3456789012", "4567890123"]
    #     for p in phones:           
    #         _user = M.UserProfile.objects.get(phone=p)
    #         _seats = M.Seat.objects.get(row_id='A', col_id=3)
    #         _type = M.SeatType.objects.get(name="Regular")
    #         _show = M.Show.objects.get(time='10:00:00')
    #         _booking = M.Booking.objects.create(user=_user, seats=_seats, show=_show, type=_type)
    #         _booking.save()

    def seed(self, path):
        paths=path.split(',')
        df1 = pd.read_csv(paths[0])
        df2 = pd.read_csv(paths[1])
        # self._seed_cast_type()
        # self._seed_gender()
        # self._seed_languages(df["language"])
        # self._seed_status_type()
        # crew_profile_params=[1,10,6,14]
        # cpp = df.iloc[:, crew_profile_params]
        # self._seed_crew_profile(cpp)
        # self._seed_genres(df["genres"])
        # self._seed_user_profile()
        # crew_params=[1,10,6,14]
        # cp = df.iloc[:, crew_params]
        # self._seed_crew(cp)
        # movie_params = [11, 19, 9, 1, 10, 6, 14]
        # ms = df.iloc[:, movie_params]
        # self._seed_movies(ms)
        self._seed_city(df1["city"])
        self._seed_location(df1)
        self._seed_seat_type()
        self._seed_theater(df2)
        self._seed_screens()
        self._seed_seat()
        self._seed_shows()
    
# 0 color
# 1 director_name
# 2 num_critic_for_reviews
# 3 duration
# 4 director_facebook_likes
# 5 actor_3_facebook_likes
# 6 actor_2_name
# 7 actor_1_facebook_likes
# 8 gross
# 9 genres
# 10 actor_1_name
# 11 movie_title
# 12 num_voted_users
# 13 cast_total_facebook_likes
# 14 actor_3_name
# 15 facenumber_in_poster
# 16 plot_keywords
# 17 movie_imdb_link
# 18 num_user_for_reviews
# 19 language
# 20 country
# 21 content_rating
# 22 budget
# 23 title_year
# 24 actor_2_facebook_likes
# 25 imdb_score
# 26 aspect_ratio
# 27 movie_facebook_likes
