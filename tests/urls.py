from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    url(r"video/", include("video.urls"))  # noqa
)
