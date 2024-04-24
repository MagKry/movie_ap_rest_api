from datetime import datetime, timedelta
from random import choice

import pytest
import pytz
import json
from django.test import TestCase
from django.utils import timezone
from django.utils.lorem_ipsum import words

from showtimes.models import Cinema, Screening
from movielist.models import Movie, Person
from showtimes.tests.utils import fake_cinema_data, fake_screening_data, faker

from moviebase.settings import TIME_ZONE

TZ = pytz.timezone(TIME_ZONE)

# Create your tests here.
@pytest.mark.django_db
def test_create_cinema(client, set_up):
    cinemas_before = Cinema.objects.count()
    new_cinema = fake_cinema_data()
    response = client.post("/cinemas/", new_cinema, format='json')
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_before + 1



@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    response = client.get('/cinemas/', {}, format='json')
    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f'/cinema/{cinema.id}/', {}, format='json')

    assert response.status_code == 200
    for field in ("name", "city", "movies"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f'/cinema/{cinema.id}/', {}, format='json')

    assert response.status_code == 204
    cinema_ids = [cinema.id for cinema in Cinema.objects.all()]
    assert cinema.id not in cinema_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f'/cinema/{cinema.id}/', {}, format='json')
    cinema_data = response.data
    new_name = words(1)
    cinema_data['name'] = new_name
    new_city = 'Warszawa'
    cinema_data['city'] = new_city
    response = client.patch(f'/cinema/{cinema.id}/', cinema_data, format='json')
    new_cinema = Cinema.objects.get(id=cinema.id)

    assert response.status_code == 200
    assert new_cinema.name == new_name, new_cinema.city == new_city


@pytest.mark.django_db
def test_add_screening(client, set_up):
    screenings_count = Screening.objects.count()
    new_screening_data = {
        "cinema": Cinema.objects.first().name,
        "movie": Movie.objects.first().title,
        "date": faker.date_time(tzinfo=TZ).isoformat()
    }
    response = client.post("/screenings/", new_screening_data, format='json')
    assert response.status_code == 201
    assert Screening.objects.count() == screenings_count + 1
    new_screening_data["date"] = new_screening_data["date"].replace('+00:00', 'Z')
    for key, value in new_screening_data.items():
        assert key in response.data
        assert response.data[key] == value

'''
-----
new_screening_data["date"] = new_screening_data["date"].replace('+00:00', 'Z') – ponieważ data jest w inny sposób
trzymana w bazie, musimy zastosować takie obejście, w celu zachowania poprawności testu. Moglibyśmy oczywiście porównać
obiekty datetime, ale tak jest dużo prościej.

'''


@pytest.mark.django_db
def test_get_screening_list(client, set_up):
    response = client.get('/screenings/', {}, format='json')
    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_screening_detail(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f'/screening/{screening.id}/', {}, format='json')

    assert response.status_code == 200
    for field in ('movie', 'cinema', 'date'):
        assert field in response.data


@pytest.mark.django_db
def test_delete_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.delete(f'/screening/{screening.id}/', {}, format='json')
    assert response.status_code == 204
    screening_ids = [screening.id for screening in Screening.objects.all()]
    assert screening.id not in screening_ids


@pytest.mark.django_db
def test_update_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f'/screening/{screening.id}/', {}, format='json')
    screening_data = response.data

    new_cinema = Cinema.objects.last()
    screening_data['cinema'] = new_cinema.name
    new_movie = Movie.objects.last()
    screening_data['movie'] = new_movie.title

    response = client.patch(f'/screening/{screening.id}/', screening_data, format='json')

    assert response.status_code == 200
    new_screening = Screening.objects.get(id=screening.id)
    assert new_screening.cinema == new_cinema
    assert new_screening.movie == new_movie


@pytest.mark.django_db
def test_screening_dates_in_next_30_days(client, set_up):
    screening = Screening.objects.first()
    max_date = timezone.now() + timedelta(days=30)
    min_date = timezone.now()
    assert screening.date.strftime("%Y-%m-%dT%H:%M") <= max_date.strftime("%Y-%m-%dT%H:%M")
    assert screening.date.strftime("%Y-%m-%dT%H:%M") >= min_date.strftime("%Y-%m-%dT%H:%M")

@pytest.mark.django_db
def test_screening_list_filter_by_movie_title(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f'/screening/{screening.id}/', {}, format='json')
    screening_data = json.loads(response.content)
    assert screening.movie.title == screening_data['movie']

