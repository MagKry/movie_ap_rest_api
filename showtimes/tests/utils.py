from random import choice, sample
from faker import Faker
from django.utils import timezone

from movielist.models import Movie
from showtimes.models import Cinema, Screening

faker = Faker()

def random_movies():
    # movies = Movie.objects.all()
    # return choice(movies) - zwraca 1 obiekt
    movies = list(Movie.objects.all())
    return sample(movies, 3) #zwraca kilka - tyle ile wynosi k

def add_screenings(cinema):
    movies = random_movies()
    cinema = Cinema.objects.create(**fake_cinema_data())
    for movie in movies:
        screening = Screening.objects.create(movie=movie, cinema=cinema, date=faker.date_time())

def fake_cinema_data():
    fake_cinema_data = {
        "name": faker.name(),
        "city": faker.city(),
    }
    return fake_cinema_data


def fake_screening_data():
    cinema = Cinema.objects.create(**fake_cinema_data())
    date = faker.date_time
    fake_screening_data = {
        'movie': random_movies(),
        'cinema': cinema,
        'date': date,
    }
    return fake_screening_data

def create_fake_screening():
    screening_data = fake_screening_data()
    movie = screening_data['movie']
    cinema = screening_data['cinema']
    date = screening_data['date']
    new_screening = Screening.objects.create(movie=movie, cinema=cinema, date=date)
    return new_screening



def create_fake_cinema():
    new_cinema = Cinema.objects.create(**fake_cinema_data())
    movie = Movie.objects.first()
    date = timezone.now()
    screening = Screening.objects.create(movie=movie, cinema=new_cinema, date=date)
    new_cinema.movies.add(movie)
    return new_cinema