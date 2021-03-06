import json
import pytest

from django.core.urlresolvers import reverse

from zencoder.models import Job, Video
from zencoder.conf import settings

from httmock import urlmatch, HTTMock, response

SAMPLE_JOB_RESPONSE = {
    "id": 93541697,
    "outputs": [{
        "label": "mp4",
        "url": "http://example.com/hd.mp4",
        "id": 24211926
    }]
}

SAMPLE_NOTIFICATION_RESPONSE = {
    "outputs": [
        {
            "state": "finished",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_playlist.m3u8",
            "id": 245725936,
            "label": "application/x-mpegURL"
        },
        {
            "audio_bitrate_in_kbps": 60,
            "state": "finished",
            "file_size_in_bytes": 119557,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_64k.m3u8",
            "audio_sample_rate": 22050,
            "id": 245725929,
            "duration_in_ms": 15100
        },
        {
            "frame_rate": 30.0,
            "width": 640,
            "audio_bitrate_in_kbps": 99,
            "state": "finished",
            "file_size_in_bytes": 1688358,
            "channels": "2",
            "format": "mpeg4",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/sd.mp4",
            "total_bitrate_in_kbps": 886,
            "video_codec": "h264",
            "video_bitrate_in_kbps": 787,
            "height": 272,
            "audio_sample_rate": 48000,
            "id": 245725927,
            "duration_in_ms": 15232,
            "label": "video/mp4"
        },
        {
            "frame_rate": 15.0,
            "width": 400,
            "audio_bitrate_in_kbps": 54,
            "state": "finished",
            "file_size_in_bytes": 481064,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_240k.m3u8",
            "video_codec": "h264",
            "height": 170,
            "audio_sample_rate": 22050,
            "id": 245725930,
            "duration_in_ms": 15266
        },
        {
            "frame_rate": 30.0,
            "width": 400,
            "audio_bitrate_in_kbps": 54,
            "state": "finished",
            "file_size_in_bytes": 852740,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_440k.m3u8",
            "video_codec": "h264",
            "height": 170,
            "audio_sample_rate": 22050,
            "id": 245725931,
            "duration_in_ms": 15100
        },
        {
            "frame_rate": 30.0,
            "width": 752,
            "audio_bitrate_in_kbps": 54,
            "state": "finished",
            "file_size_in_bytes": 3744182,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_2040k.m3u8",
            "video_codec": "h264",
            "height": 320,
            "audio_sample_rate": 22050,
            "id": 245725935,
            "duration_in_ms": 15100
        },
        {
            "frame_rate": 30.0,
            "width": 752,
            "audio_bitrate_in_kbps": 54,
            "state": "finished",
            "file_size_in_bytes": 2884834,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_1540k.m3u8",
            "video_codec": "h264",
            "height": 320,
            "audio_sample_rate": 22050,
            "id": 245725934,
            "duration_in_ms": 15100
        },
        {
            "frame_rate": 30.0,
            "width": 640,
            "audio_bitrate_in_kbps": 53,
            "state": "finished",
            "file_size_in_bytes": 2011574,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_1040k.m3u8",
            "video_codec": "h264",
            "height": 272,
            "audio_sample_rate": 22050,
            "id": 245725933,
            "duration_in_ms": 15100
        },
        {
            "frame_rate": 30.0,
            "width": 640,
            "audio_bitrate_in_kbps": 112,
            "state": "finished",
            "file_size_in_bytes": 1636802,
            "channels": "2",
            "format": "webm",
            "audio_codec": "vorbis",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/sd.webm",
            "total_bitrate_in_kbps": 819,
            "video_codec": "vp8",
            "video_bitrate_in_kbps": 707,
            "height": 272,
            "audio_sample_rate": 48000,
            "id": 245725928,
            "duration_in_ms": 15189,
            "label": "video/webm"
        },
        {
            "frame_rate": 30.0,
            "width": 480,
            "audio_bitrate_in_kbps": 54,
            "state": "finished",
            "file_size_in_bytes": 1256376,
            "channels": "2",
            "format": "mpeg-ts",
            "audio_codec": "aac",
            "url": "http://onionwebtech.s3.amazonaws.com/videoads/360/hls_640k.m3u8",
            "video_codec": "h264",
            "height": 204,
            "audio_sample_rate": 22050,
            "id": 245725932,
            "duration_in_ms": 15100
        }
    ],
    "input": {
        "frame_rate": 30.0,
        "width": 752,
        "audio_bitrate_in_kbps": 167,
        "state": "finished",
        "file_size_in_bytes": 2684145,
        "channels": "2",
        "format": "mpeg4",
        "audio_codec": "aac",
        "total_bitrate_in_kbps": 1410,
        "video_codec": "h264",
        "video_bitrate_in_kbps": 1243,
        "height": 320,
        "audio_sample_rate": 48000,
        "id": 93717775,
        "duration_in_ms": 15168
    },
    "job": {
        "test": False,
        "submitted_at": "2014-05-13T20:17:30Z",
        "state": "finished",
        "created_at": "2014-05-13T20:17:30Z",
        "pass_through": None,
        "updated_at": "2014-05-13T20:18:46Z",
        "id": 93541697
    }
}


@urlmatch(netloc=r'app\.zencoder\.com$', path="/api/v2/jobs")
def zencoder_jobs_mock(url, request):

    headers = {'content-type': 'application/json'}
    return response(status_code=201, content=SAMPLE_JOB_RESPONSE, headers=headers, request=request)


@pytest.mark.django_db
def test_video_api(admin_client):
    video = Video.objects.create(input="s3://example.com/input.mp4")
    video_endpoint = reverse("zencoder.views.video", kwargs={"video_id": video.id})

    response = admin_client.get(video_endpoint)
    assert response.status_code == 200
    data = json.loads(response.content.decode("utf-8"))
    assert data["poster"] is None

    response = admin_client.post(video_endpoint, {"poster": "http://www.example.com/poster.jpeg"})
    assert response.status_code == 200
    data = json.loads(response.content.decode("utf-8"))
    assert data["poster"] == "http://www.example.com/poster.jpeg"

    response = admin_client.get(video_endpoint)
    assert response.status_code == 200
    data = json.loads(response.content.decode("utf-8"))
    assert data["poster"] == "http://www.example.com/poster.jpeg"


@pytest.mark.django_db
def test_encode_endpoint():

    if settings.ZENCODER_API_KEY is None:
        return

    settings.ZENCODER_JOB_PAYLOAD["mock"] = True

    video = Video.objects.create(input="s3://example.com/input.mp4")
    Job.objects.start(video=video)

    del settings.ZENCODER_JOB_PAYLOAD["mock"]


@pytest.mark.django_db
def test_start_encode(admin_client):

    # First, let's mock the start of the encoding.
    video = Video.objects.create(input="s3://example.com/input.mp4")
    with HTTMock(zencoder_jobs_mock):

        encode_endpoint = reverse("zencoder.views.encode", kwargs={"video_id": video.id})
        response = admin_client.post(encode_endpoint)
        assert response.status_code == 200
        data = json.loads(response.content.decode("utf-8"))
        assert data["json"] == "https://app.zencoder.com/api/v2/jobs/93541697/progress.json?api_key={}".format(settings.ZENCODER_API_KEY)

        job = Job.objects.get(video=video)
        assert job.status == Job.IN_PROGRESS
        assert job.job_id == 93541697
        assert job.data == SAMPLE_JOB_RESPONSE

    # Now, let's simulate a notification callback from zencoder
    notify_endpoint = reverse("zencoder.views.notify")
    response = admin_client.post(notify_endpoint, json.dumps(SAMPLE_NOTIFICATION_RESPONSE), content_type="application/json")
    assert response.status_code == 204
    assert video.sources.count() == 3
    job = Job.objects.get(id=job.id)  # refresh from the db
    assert job.status == Job.COMPLETE
