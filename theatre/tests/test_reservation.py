import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User
from theatre.models import Play, TheatreHall, Performance, Reservation, Ticket
from django.utils import timezone
from datetime import timedelta


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


@pytest.mark.django_db
def test_reservation_create(auth_client, user, performance):
    url = reverse("reservation-list")
    data = {
        "tickets": [
            {"row": 1, "seat": 1, "performance": performance.id},
            {"row": 1, "seat": 2, "performance": performance.id},
        ]
    }
    response = auth_client.post(url, data, format="json")

    assert response.status_code == 201
    assert Reservation.objects.count() == 1
    assert Ticket.objects.count() == 2
    reservation = Reservation.objects.first()
    assert reservation.user == user


@pytest.mark.django_db
def test_reservation_requires_auth(api_client, performance):
    url = reverse("reservation-list")
    data = {"tickets": [{"row": 1, "seat": 1, "performance": performance.id}]}
    response = api_client.post(url, data, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_double_book(auth_client, user, performance):
    reservation = Reservation.objects.create(user=user)
    Ticket.objects.create(
        reservation=reservation, performance=performance, row=1, seat=1
    )

    url = reverse("reservation-list")
    data = {"tickets": [{"row": 1, "seat": 1, "performance": performance.id}]}
    response = auth_client.post(url, data, format="json")

    assert response.status_code == 400
    assert Ticket.objects.count() == 1
