from django.urls import reverse

from theatre.models import Reservation, Ticket
from theatre.tests.test_base import *  # noqa: F403,F405


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
