import pytest

from django.core.urlresolvers import reverse

from zencoder.models import Video, Source, Job


@pytest.mark.django_db
def test_video_embed_params(client):
    video = Video.objects.create(input="s3://example.com/input.mp4")
    Source.objects.create(video=video, url="http://example.com/output.mp4", content_type="video/mp4")
    Source.objects.create(video=video, url="http://example.com/output.webm", content_type="video/webm")
    Source.objects.create(video=video, url="http://example.com/output.m3u8", content_type="application/x-mpegURL")

    id_param = "{}///".format(video.id)

    video_embed_url = "{endpoint}?id={id}".format(
        endpoint=reverse("zencoder.views.embed"),
        id=id_param)

    response = client.get(video_embed_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_video_embed(client):

    video = Video.objects.create(input="s3://example.com/input.mp4")

    video_embed_url = "{endpoint}?id={id}".format(
        endpoint=reverse("zencoder.views.embed"),
        id=video.id)
    
    response = client.get(video_embed_url)
    assert "X-Frame-Options" not in response
    assert response.status_code == 500

    # Now we add some sources
    Source.objects.create(video=video, url="http://example.com/output.mp4", content_type="video/mp4")
    Source.objects.create(video=video, url="http://example.com/output.webm", content_type="video/webm")
    Source.objects.create(video=video, url="http://example.com/output.m3u8", content_type="application/x-mpegURL")

    response = client.get(video_embed_url)
    assert response.status_code == 200

    job = Job.objects.create(video=video, status=Job.IN_PROGRESS, job_id="12345")
    response = client.get(video_embed_url)
    assert response.template_name[0] == "zencoder/embed/encoding.html"
    assert response.status_code == 202

    job.status = Job.FAILED
    job.save()
    response = client.get(video_embed_url)
    assert response.template_name[0] == "zencoder/embed/failed.html"
    assert response.status_code == 500

    job.status = Job.NOT_STARTED
    job.save()
    response = client.get(video_embed_url)
    assert response.template_name[0] == "zencoder/embed/failed.html"
    assert response.status_code == 500

    job.status = Job.COMPLETE
    job.save()
    response = client.get(video_embed_url)
    assert response.template_name[0] == "zencoder/embed/video.html"
    assert response.template_name[1] == "zencoder/embed/default.html"
    assert response.status_code == 200

