import pytest

from django.core.urlresolvers import reverse

from zencoder.models import Source, Video


def create_test_data():
    video = Video.objects.create(
        duration=100,
        input="s3:/example.com/input.mp4",
        name="Some video.",
        poster="http://yestheposter.com",

    )
    sources = [
        Source.objects.create(
            video=video,
            url="http://example.com/output.mp4",
            content_type="video/mp4"
        ),
        Source.objects.create(
            video=video,
            url="http://example.com/output.webm",
            content_type="video/webm"
        ),
        Source.objects.create(
            video=video,
            url="http://example.com/output.m3u8",
            content_type="application/x-mpegURL"
        ),
    ]
    return {
        "video": video,
        "sources": sources
    }


@pytest.mark.django_db
def test_video_json(client):
    test_data = create_test_data()
    video_json_url = reverse("video-json", kwargs={"video_id": test_data["video"].id})
    resp = client.get(video_json_url)
    assert resp.status_code == 200
    data = resp.data

    # Placeholder values
    assert data["category"] == ""
    assert data["channel_logo_url"] == ""
    assert data["channel_name"] == ""
    assert data["channel_slug"] == ""
    assert data["channel_url"] == ""
    assert data["description"] == ""
    assert data["player_options"] == {}
    assert data["season"] == ""
    assert data["series_logo_url"] == ""
    assert data["series_name"] == ""
    assert data["series_slug"] == ""
    assert data["series_url"] == ""
    assert data["sponsor_id"] is None
    assert data["tags"] == []
    assert data["targeting"] == {}
    assert data["tunic_campaign_url"] is None

    # Model values
    assert data["duration"] == test_data["video"].duration
    assert data["id"] == test_data["video"].id
    assert data["input"] == test_data["video"].input
    assert data["name"] == test_data["video"].name
    assert data["title"] == test_data["video"].name
    assert data["poster"] == test_data["video"].poster
    assert data["poster_url"] == test_data["video"].poster
    assert len(data["sources"]) == len(test_data["sources"])
