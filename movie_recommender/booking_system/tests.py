from django.test import TestCase
from .management.commands import seed
from .models import *
from .views import *
from functors.booker import Booker
from django.test.utils import override_settings
import threading

def test_concurrently(times):
    """
    Add this decorator to small pieces of code that you want to test
    concurrently to make sure they don't raise exceptions when run at the
    same time.  E.g., some Django views that do a SELECT and then a subsequent
    INSERT might fail when the INSERT assumes that the data has not changed
    since the SELECT.
    """
    def test_concurrently_decorator(test_func):
        def wrapper():
            exceptions = []
            def call_test_func(i):
                try:
                    test_func(i)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func, args=[i]))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator

# Create your tests here.
class TestConcurrency(TestCase):
    def setUp(self):
        command = seed.Command()
        command.seed("seed/movie_metadata.csv")


    def temp_test(self):
        seats = Seat.objects.all()[:5]
        show = seats[0].screen.show_set.all()[0]
        users = UserProfile.objects.all()

        data = {
            users[0].id: (show.id, [seats[0].id, seats[1].id]),
            users[1].id: (show.id, [seats[2].id, seats[1].id]),
            users[2].id: (show.id, [seats[3].id, seats[4].id])
        }
        user_ids = [i.id for i in users]
        booker = Booker()
        bookings = [booker.start_booking(show, users[i]).id for i in range(3)]

        last_run = -1

        @test_concurrently(3)
        def check_race_condition(i):
            user_id = user_ids[i]
            show_id, seat_ids = data[user_id]
            booker.select(bookings[i], seat_ids[0], user_id)
            booker.select(bookings[i], seat_ids[1], user_id)
            if i != 2:
                last_run = user_id

        check_race_condition()
        assert Booking.objects.filter(pk=bookings[last_run]).count() == 0
