import json
import pytest

from video.models import Job, Video

from httmock import urlmatch, HTTMock, response


@urlmatch(netloc=r'app\.zencoder\.com$', path="/api/v2/jobs")
def zencoder_jobs_mock(url, request):

    content = json.dumps({
        "id": 93541697,
        "outputs": [{
            "label": "mp4",
            "url": "http://example.com/hd.mp4",
            "id": 24211926
        }]
    })
    headers = {'content-type': 'application/json'}
    return response(201, content, headers, None, 5, request)


@pytest.mark.django_db
def test_start_endcode(settings):
    settings.ZENCODER_API_KEY = "abcde12345"

    video = Video.objects.create(input="s3://example.com/input.mp4")
    with HTTMock(zencoder_jobs_mock):
        job = Job.objects.create_from_video(video)
        assert job.status == Job.IN_PROGRESS
        assert job.job_id == "93541697"
