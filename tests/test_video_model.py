import json
import pytest

from django.core.urlresolvers import reverse

from zencoder.models import Video, Source
from zencoder.conf import settings


@pytest.mark.django_db
def test_video_sorting():
    video = Video.objects.create(input="s3://example.com/input.mp4")
    Source.objects.create(video=video, url="http://example.com/output.mp4", content_type="video/mp4")
    Source.objects.create(video=video, url="http://example.com/output.webm", content_type="video/webm")
    Source.objects.create(video=video, url="http://example.com/output.m3u8", content_type="application/x-mpegURL")

    assert video.ordered_sources()[0].content_type == "video/mp4"
    assert video.ordered_sources()[1].content_type == "video/webm"
    assert video.ordered_sources()[2].content_type == "application/x-mpegURL"


@pytest.mark.django_db
def test_video_endpoint(admin_client):

    new_endpoint = reverse("video-new")
    response = admin_client.post(new_endpoint, data={"name": "test.flv"})
    assert response.status_code == 201
    data = json.loads(response.content.decode("utf-8"))
    video_id = data.get("id")

    expected_path = "{}/{}/{}/test.flv".format(
        settings.VIDEO_ENCODING_BUCKET,
        settings.VIDEO_ENCODING_DIRECTORY,
        video_id)
    assert data.get("path").endswith(expected_path)
    
    video = Video.objects.get(pk=video_id)
    assert video.name == "test.flv"

    detail_endpoint = reverse("video-detail", kwargs={"video_id": video.id})
    response = admin_client.post(detail_endpoint, data={"name": "test2.flv"})
    video = Video.objects.get(pk=video_id)
    assert video.name == "test2.flv"

