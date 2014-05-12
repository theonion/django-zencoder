import json
import requests

from django.core.urlresolvers import reverse

from .conf import settings


class TranscoderBase(object):

    class Meta:
        abstract = True

    def __init__(self, job_id=None):
        self.job_id = job_id

    def start(self, input_url):
        """Starts a transcoding job"""
        raise NotImplemented()

    def cancel(self):
        raise NotImplemented()


class Zencoder(TranscoderBase):

    AUTH_HEADERS = {'Zencoder-Api-Key': settings.ZENCODER_API_KEY}

    def start(self, input_url, output_url):
        payload = {
            "input": input_url,
            "base_url": output_url,
            "outputs": settings.ZENCODER_OUTPUTS,
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

    def cancel(self):
        url = "https://app.zencoder.com/api/v2/jobs/{}/cancel.json".format(self.job_id)
        response = requests.put(url, headers=self.AUTH_HEADERS)
        if response.status_code != 204:
            raise Exception("Couldn't cancel the job!")





