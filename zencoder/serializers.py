from rest_framework import serializers

from .models import Source, Video


class ZencoderSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source


class ZencoderVideoSerializer(serializers.ModelSerializer):

    sources = ZencoderSourceSerializer(many=True)

    class Meta:
        model = Video
