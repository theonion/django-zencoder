import pytest

from zencoder.models import Source, Video
from zencoder.serializers import ZencoderVideoSerializer


@pytest.mark.django_db
def test_video_serializer():
    video = Video.objects.create(
        duration=100,
        input="s3:/example.com/input.mp4",
        name="Some video.",
        poster="http://yestheposter.com",

    )
    Source.objects.create(
        video=video,
        url="http://example.com/output.mp4",
        content_type="video/mp4"
    )
    Source.objects.create(
        video=video,
        url="http://example.com/output.webm",
        content_type="video/webm"
    )
    Source.objects.create(
        video=video,
        url="http://example.com/output.m3u8",
        content_type="application/x-mpegURL"
    )

    data = ZencoderVideoSerializer().to_representation(video)
    assert data["duration"] == video.duration
    assert data["id"] == video.id
    assert data["input"] == video.input
    assert data["name"] == video.name
    assert data["poster"] == video.poster
