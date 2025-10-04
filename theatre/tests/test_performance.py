from django.urls import reverse

from theatre.tests.test_base import *  # noqa: F403,F405


@pytest.mark.django_db
def test_get_performance_detail(api_client, performance):
    url = reverse("performance-detail", args=[performance.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["play"]["id"] == performance.play.id


@pytest.mark.django_db
def test_get_performance_list(api_client, performance):
    url = reverse("performance-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert any(p["id"] == performance.id for p in response.data)


@pytest.mark.django_db
def test_filter_performance_by_play(api_client, performance):
    url = reverse("performance-list")
    response = api_client.get(url, {"play": performance.play.id})
    assert response.status_code == 200
    assert all(p["play"]["id"] == performance.play.id for p in response.data)


@pytest.mark.django_db
def test_filter_performance_by_date(api_client, performance):
    url = reverse("performance-list")
    show_date = performance.show_time.date().isoformat()
    response = api_client.get(url, {"date": show_date})
    assert response.status_code == 200
    assert all(p["show_time"].startswith(show_date) for p in response.data)


@pytest.mark.django_db
def test_performance_detail_not_found(api_client):
    url = reverse("performance-detail", args=[999])
    response = api_client.get(url)
    assert response.status_code == 404