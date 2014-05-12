import json
import requests

from django.core.urlresolvers import reverse

from .conf import settings


class TranscoderBase(object):

    class Meta:
        abstract = True

    def __init__(self, job_id=None):
        self.job_id = job_id

    def start(self, input_url, output_url):
        """Starts a transcoding job"""
        raise NotImplemented()

    def finish(self, data):
        """Finishes a transcoding job"""
        raise NotImplemented()

    def cancel(self):
        """Cancels a transcoding job"""
        raise NotImplemented()


class Zencoder(TranscoderBase):

    AUTH_HEADERS = {'Zencoder-Api-Key': settings.ZENCODER_API_KEY}

    def start(self, input_url, output_url):
        payload = {
            "input": input_url,
            "base_url": output_url,
            "outputs": self.get_outputs(),
            "notifications": [{
                "url": reverse("video.views.notify", kwargs={"transcoder": "video.transcoders.Zencoder"})
            }]
        }

        response = requests.post(
            "https://app.zencoder.com/api/v2/jobs",
            data=json.dumps(payload),
            headers=self.AUTH_HEADERS)

        if response.status_code != 201:
            raise Exception("Zencoder response {}".format(response.status_code))
        
        self.job_id = str(response.json().get('id'))
        return self.job_id, response.json()

    def finish(self, data):
        sources = []
        for output in data.get("outputs", []):
            if output["label"] in ("video/mp4", "video/webm", "application/x-mpegURL"):
                sources.append({
                    "url": output["url"],
                    "width": output["width"],
                    "content_type": output["label"]
                })
        return sources
        
    def cancel(self):
        url = "https://app.zencoder.com/api/v2/jobs/{}/cancel.json".format(self.job_id)
        response = requests.put(url, headers=self.AUTH_HEADERS)
        if response.status_code != 204:
            raise Exception("Couldn't cancel the job!")

    def get_outputs(self):
        return [
            {"thumbnails": {"number": 20, "width": 1024, "prefix": "thumbnail"}},
            {"format": "mp4", "filename": "640.mp4", "width": 640, "label": "video/mp4"},
            {"format": "webm", "filename": "640.webm", "width": 640, "label": "video/webm"},
            {"format": "aac", "filename": 'hls_64k.m3u8', "audio_bitrate": 64, "audio_sample_rate": 22054, "type": "segmented"},
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 184,
                "decoder_buffer_size": 840,
                "filename": "hls_240k.m3u8",
                "width": 400,
                "max_frame_rate": 15,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 360,
            },
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 384,
                "decoder_buffer_size": 1344,
                "filename": "hls_440k.m3u8",
                "width": 400,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 578,
            },
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 584,
                "decoder_buffer_size": 2240,
                "filename": "hls_640k.m3u8",
                "width": 480,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 960,
            },
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 1000,
                "decoder_buffer_size": 4000,
                "filename": "hls_1040k.m3u8",
                "width": 640,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 1500,
            },
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 1484,
                "decoder_buffer_size": 5390,
                "filename": "hls_1540k.m3u8",
                "width": 960,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 2310,
            },
            {
                "format": "ts",
                "type": "segmented",
                "video_bitrate": 1984,
                "decoder_buffer_size": 7140,
                "filename": "hls_2040k.m3u8",
                "width": 1024,
                "audio_bitrate": 56,
                "audio_sample_rate": 22050,
                "decoder_bitrate_cap": 3060,
            },
            {
                "label": "application/x-mpegURL",
                "type": "playlist",
                "streams": [
                    {"path": "hls_2040k.m3u8", "bandwidth": 2040},
                    {"path": "hls_1540k.m3u8", "bandwidth": 1540},
                    {"path": "hls_1040k.m3u8", "bandwidth": 1040},
                    {"path": "hls_640k.m3u8", "bandwidth": 640},
                    {"path": "hls_440k.m3u8", "bandwidth": 440},
                    {"path": "hls_240k.m3u8", "bandwidth": 240},
                    {"path": "hls_64k.m3u8", "bandwidth": 64}
                ],
                "filename": "hls_playlist.m3u8"
            }
        ]



