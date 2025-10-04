from theatre.models import Play, TheatreHall, Performance
from user.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="testuser@test.com", password="pass123"
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def play(db):
    return Play.objects.create(
        title="Hamlet", description="Tragedy by Shakespeare"
    )


@pytest.fixture
def hall(db):
    return TheatreHall.objects.create(name="Main Hall", rows=5, seats_in_row=5)


@pytest.fixture
def performance(play, hall):
    return Performance.objects.create(
        play=play,
        theatre_hall=hall,
        show_time=timezone.now() + timedelta(days=1),
    )



