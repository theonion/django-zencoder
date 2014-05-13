import json
import pytest

from video.models import Job, Video

from httmock import urlmatch, HTTMock, response

SAMPLE_JOB_RESPONSE = {
    "id": 93541697,
    "outputs": [{
        "label": "mp4",
        "url": "http://example.com/hd.mp4",
        "id": 24211926
    }]
}


@urlmatch(netloc=r'app\.zencoder\.com$', path="/api/v2/jobs")
def zencoder_jobs_mock(url, request):

    content = json.dumps(SAMPLE_JOB_RESPONSE)
    headers = {'content-type': 'application/json'}
    return response(status_code=201, content=content, headers=headers, request=request)


@pytest.mark.django_db
def test_start_endcode(settings):
    settings.ZENCODER_API_KEY = "abcde12345"

    # First, let's mock the start of the encoding.
    video = Video.objects.create(input="s3://example.com/input.mp4")
    with HTTMock(zencoder_jobs_mock):
        job = Job.objects.start(video)
        assert job.status == Job.IN_PROGRESS
        assert job.job_id == 93541697
        assert job.data == SAMPLE_JOB_RESPONSE
