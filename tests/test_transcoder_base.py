from video.models import Video, Job
from video.transcoders import TranscoderBase


class TestTranscoder(TranscoderBase):

    def start(self, input_url):
        return 10

    def error(self, *args, **kwargs):
        """Reports an error, and updates the video status"""
        raise NotImplemented()

    def success(self, *args, **kwargs):
        """This is called after a video is transcoded sucessfully"""
        raise NotImplemented()


def test_something():
    video = Video(input="http://example.com/test.mp4")
