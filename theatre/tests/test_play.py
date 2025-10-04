from django.urls import reverse

from theatre.tests.test_base import *  # noqa: F403,F405


@pytest.mark.django_db
def test_get_plays_list(api_client, play):
    url = reverse("play-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == play.title


@pytest.mark.django_db
def test_get_play_detail(api_client, play):
    url = reverse("play-detail", args=[play.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == play.title
    assert response.data["description"] == play.description


@pytest.mark.django_db
def test_search_play_by_title(api_client, play):
    url = reverse("play-list")
    response = api_client.get(url, {"search": "Hamlet"})
    assert response.status_code == 200
    assert any("Hamlet" in p["title"] for p in response.data)


@pytest.mark.django_db
def test_ordering_plays_by_title(api_client, play):
    Play.objects.create(title="A Play", description="Test play")
    url = reverse("play-list")
    response = api_client.get(url, {"ordering": "title"})
    titles = [p["title"] for p in response.data]
    assert titles == sorted(titles)


@pytest.mark.django_db
def test_create_play_admin_only(api_client, play):
    url = reverse("play-list")
    data = {"title": "New Play", "description": "New Desc"}
    response = api_client.post(url, data, format="json")
    assert response.status_code in [401, 403]