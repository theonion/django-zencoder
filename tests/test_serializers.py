import pytest

from zencoder.models import Source, Video
from zencoder.serializers import ZencoderSourceSerializer, ZencoderVideoSerializer


def serializer_test_data():
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
def test_source_serializer():
    test_data = serializer_test_data()
    source = test_data["sources"][0]
    data = ZencoderSourceSerializer().to_representation(source)
    assert data["bitrate"] == source.bitrate
    assert data["content_type"] == source.content_type
    assert data["url"] == source.url
    assert data["width"] == source.width


@pytest.mark.django_db
def test_video_serializer():
    test_data = serializer_test_data()
    data = ZencoderVideoSerializer().to_representation(test_data["video"])
    assert data["duration"] == test_data["video"].duration
    assert data["id"] == test_data["video"].id
    assert data["input"] == test_data["video"].input
    assert data["name"] == test_data["video"].name
    assert data["poster"] == test_data["video"].poster
