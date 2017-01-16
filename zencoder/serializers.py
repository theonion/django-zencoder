from rest_framework import serializers

from .models import Video


class ZencoderVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
