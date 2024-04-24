import os
import sys

import pytest
from rest_framework.test import APIClient

from showtimes.tests.utils import faker, create_fake_cinema, add_screenings
from showtimes.models import Cinema
from movielist.models import Person
from movielist.tests.utils import create_fake_movie

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = APIClient()
    return client


# @pytest.fixture # moje
# def set_up():
#     for _ in range(5):
#         Cinema.objects.create(name=faker.name())
#     for _ in range(3):
#         create_fake_cinema()

@pytest.fixture
def set_up():
    for _ in range(5):
        Person.objects.create(name=faker.name())
    for _ in range(10):
        create_fake_movie()
    for _ in range(3):
        create_fake_cinema()
    for _ in range(5):
        add_screenings(create_fake_cinema())

