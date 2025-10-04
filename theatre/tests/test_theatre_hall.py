from django.urls import reverse

from theatre.tests.test_base import *  # noqa: F403,F405


@pytest.mark.django_db
def test_create_theatre_hall_admin_only(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("theatrehall-list")
    data = {"name": "VIP Hall", "rows": 10, "seats_in_row": 10}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_theatre_hall_list(api_client, hall):
    url = reverse("theatrehall-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert any(h["id"] == hall.id for h in response.data)


@pytest.mark.django_db
def test_get_theatre_hall_detail(api_client, hall):
    url = reverse("theatrehall-detail", args=[hall.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == hall.name
    assert response.data["rows"] == hall.rows
    assert response.data["seats_in_row"] == hall.seats_in_row


@pytest.mark.django_db
def test_theatre_hall_str(hall):
    assert str(hall) == hall.name
