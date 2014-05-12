import importlib

from django.db import models

from json_field import JSONField

from .conf import settings


def sort_video(source):
    try:
        weight = settings.VIDEO_PREFERENCES.index(source.content_type)
    except:
        weight = len(settings.VIDEO_PREFERENCES) + 1
    return weight * (source.width or 1)


class Video(models.Model):
    """This is a very lightweight model that basically wraps an externally available set of sources
    for a given video."""

    name = models.CharField(max_length=255)
    poster = models.URLField(null=True, blank=True)
    input = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def ordered_sources(self):
        return sorted(list(self.sources.all()), key=sort_video)


class Source(models.Model):
    video = models.ForeignKey(Video, related_name="sources")
    url = models.URLField()
    content_type = models.CharField(max_length=100)
    width = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True, help_text="In kilobits per second")

    class Meta:
        ordering = ("width", "bitrate")


class JobManager(models.Manager):

    def create_from_video(self, video):
        job = self.create(video=video)
        job.start()
        job.save()
        return job


class Job(models.Model):

    NOT_STARTED = 0
    COMPLETE = 1
    IN_PROGRESS = 2
    FAILED = 3
    STATUSES = (
        (NOT_STARTED, 'Not started'),
        (COMPLETE, 'Complete'),
        (IN_PROGRESS, 'In Progress'),
        (FAILED, 'Failed')
    )

    objects = JobManager()

    video = models.ForeignKey(Video)
    status = models.IntegerField(choices=STATUSES, default=NOT_STARTED, help_text="The encoding status")
    job_id = models.CharField(null=True, blank=True, max_length=255, help_text="The external job ID")
    data = JSONField(null=True, blank=True)
    transcoder_class = models.CharField(max_length=255, default=settings.VIDEO_TRANSCODER)

    @property
    def transcoder(self):
        module_name, class_name = self.transcoder_class.rsplit(".", 1)
        cls = getattr(importlib.import_module(module_name), class_name)
        return cls(job_id=self.job_id)

    def start(self):
        output_url = "s3://{}/{}/{}/".format(
            settings.VIDEO_ENCODING_BUCKET,
            settings.VIDEO_ENCODING_DIRECTORY,
            self.video.id)
        self.job_id, self.data = self.transcoder.start(self.video.input, output_url)
        self.status = self.IN_PROGRESS
        return self.data

    def cancel(self):
        self.transcoder.cancel()
        self.status = self.FAILED
