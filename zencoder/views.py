import json
import base64
import hmac
import hashlib
import datetime
import os
import re

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView

from .conf import settings
from .models import Video, Job


@csrf_exempt
def notify(request):
    data = json.loads(request.body.decode("utf-8"))
    job = get_object_or_404(Job, job_id=data.get("job", {}).get("id"))
    job.notify(data)
    job.save()
    target_video = job.video
    target_video.duration = data.get("input", {}).get("duration_in_ms")
    target_video.save()
    return HttpResponse(content="", status=204)


@require_http_methods(["POST"])
@staff_member_required
def encode(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    job = Job.objects.start(video=video)
    data = job.encode_status_endpoints()

    return HttpResponse(json.dumps(data), content_type="application/json")


@require_http_methods(["POST", "GET"])
@staff_member_required
def video(request, video_id=None):
    status_code = 200
    if request.method == "GET":
        video = get_object_or_404(Video, pk=video_id)
    elif request.method == "POST":
        if video_id is None:
            video = Video.objects.create()
            status_code = 201
        else:
            # Let's just make sure this video exists
            video = get_object_or_404(Video, pk=video_id)
        if "name" in request.POST:
            video.name = request.POST["name"]

        video.poster = request.POST.get("poster")
    else:
        return HttpResponse("")

    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    key = os.path.join(settings.VIDEO_ENCODING_DIRECTORY, str(video.id), video.name)

    video.input = "s3://{}/{}".format(settings.VIDEO_ENCODING_BUCKET, key)
    video.save()

    # Now let's build a signature for this upload, using:
    # http://docs.aws.amazon.com/AmazonS3/latest/dev/HTTPPOSTForms.html
    policy_dict = {
        "expiration": expiration.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "conditions": [
            {"bucket": settings.VIDEO_ENCODING_BUCKET},
            {"acl": "private"},
            {"success_action_status": '201'},
            {"key": key},
            ["content-length-range", 0, settings.VIDEO_ENCODING_MAX_SIZE],
        ]
    }

    policy_document = json.dumps(policy_dict).encode("utf-8")
    policy = base64.b64encode(policy_document)

    signature = hmac.new(
        settings.AWS_SECRET_ACCESS_KEY.encode("utf-8"),
        policy,
        hashlib.sha1).digest()

    upload_endpoint = "https://{}.s3.amazonaws.com".format(settings.VIDEO_ENCODING_BUCKET)

    status = "Not started"
    encode_status_endpoints = None
    if video.job_set.count() > 0:
        job = video.job_set.all()[0]
        status = job.get_status_display()
        encode_status_endpoints = job.encode_status_endpoints()

    contents = {
        "id": video.id,
        "path": video.input,
        "key": key,
        "poster": video.poster,
        "status": status,
        "encode_status_endpoints": encode_status_endpoints,
        "upload_endpoint": upload_endpoint,
        'AWSAccessKeyId': settings.AWS_ACCESS_KEY_ID,
        'acl': 'private',
        'success_action_status': '201',
        'policy': policy.decode("utf-8"),
        'signature': base64.b64encode(signature).decode("utf-8")
    }
    return HttpResponse(json.dumps(contents), status=status_code, content_type="application/json")


class VideoEmbedView(DetailView):
    model = Video
    context_object_name = "video"

    @xframe_options_exempt
    def get(self, *args, **kwargs):
        return super(VideoEmbedView, self).get(*args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.GET.get("id", "")
        """OK, don't ask me why, but there are some requests appending a "/" to
        the end of the querystring. So I'm gonna fix that for them."""

        pk = re.sub(r'[^\d.]+', '', pk)
        try:
            obj = queryset.get(pk=pk)
        except (queryset.model.DoesNotExist, ValueError):
            raise Http404("No Video found")
        return obj

    def get_template_names(self):
        names = ["zencoder/embed/video.html", "zencoder/embed/default.html"]
        if self.object.job_set.count() > 0:
            job = self.object.job_set.all()[0]
            if job.status == Job.IN_PROGRESS:
                names.insert(0, "zencoder/embed/encoding.html")
            elif job.status != Job.COMPLETE:
                names.insert(0, "zencoder/embed/failed.html")
        else:
            if self.object.sources.count() == 0:
                # Really, this has only failed if there are no sources.
                names.insert(0, "zencoder/embed/failed.html")
        return names

    def render_to_response(self, context, **response_kwargs):
        if self.object.sources.count() == 0:
            # If there aren't any sources, this is a bad video
            response_kwargs["status"] = 500

        if self.object.job_set.count() > 0:
            job = self.object.job_set.all()[0]

            if job.status == Job.IN_PROGRESS:
                # If the video is still encoding, we'll make it a 202
                response_kwargs["status"] = 202
            elif job.status != Job.COMPLETE:
                response_kwargs["status"] = 500

        response = super(VideoEmbedView, self).render_to_response(context, **response_kwargs)
        if response.status_code != 200:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response
embed = VideoEmbedView.as_view()
