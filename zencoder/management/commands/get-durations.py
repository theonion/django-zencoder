from django.core.management import BaseCommand
import os
import re
import requests
import tempfile
import subprocess

from zencoder.models import Video


DURATION_REGEX = re.compile("Duration\s+: (?P<minute>\d+)?(?:mn )?(?P<second>\d+)s")


class Command(BaseCommand):

    def get_video_duration(self, video):
        mp4_source = video.sources.filter(content_type="video/mp4").first()
        if mp4_source is None:
            print("No mp4: {}".format(video.id))
            return

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_file:
            response = requests.get(mp4_source.url, stream=True)

            for header_data in response.iter_content(chunk_size=1024):
                break

            response.close()

            video_file.write(header_data)
            video_file.close()

            try:
                output = subprocess.check_output(["mediainfo", video_file.name])
            except subprocess.CalledProcessError:
                print("Bad file: {}".format(video.pk))
                return

            match = DURATION_REGEX.search(output.decode("ascii"))
            if match:
                duration = 0
                if match.group("minute"):
                    duration += int(match.group("minute")) * 60 * 1000

                if match.group("second"):
                    duration += int(match.group("second")) * 1000

                video.duration = duration
                video.save()

        os.remove(video_file.name)

    def handle(self, *args, **options):

        videos = Video.objects.filter(duration__in=[None, 0])
        self.stdout.write('getting durations for {} videos'.format(videos.count()))

        for video in videos:
            self.get_video_duration(video)
