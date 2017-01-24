from django.conf import settings

from rest_framework import serializers

from zencoder.utils.serializers import PlaceholderFieldsMixin
from .models import Source, Video


class ZencoderSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source


class ZencoderVideoSerializer(PlaceholderFieldsMixin, serializers.ModelSerializer):

    player_options = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()
    sources = ZencoderSourceSerializer(many=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = Video
        placeholder_fields = {
            "category": "",
            "channel_logo_url": "",
            "channel_name": "",
            "channel_slug": "",
            "channel_url": "",
            "description": "",
            "season": "",
            "series_logo_url": "",
            "series_name": "",
            "series_slug": "",
            "series_url": "",
            "sponsor_id": None,
            "tags": [],
            "targeting": {},
            "tunic_campaign_url": None,
        }

    def get_player_options(self, obj):
        comscore_settings = getattr(settings, "ZENCODER_COMSCORE_SETTINGS", {})
        return {
            "comscore": {
                "id": getattr(settings, "VIDEOMETRIX_ID", None),
                "metadata": {
                    "ns_st_ci": None,
                    "c3": comscore_settings.get("channel_name", ""),
                    "c4": comscore_settings.get("channel_code", "")
                }
            }
        }

    def get_poster_url(self, obj):
        return getattr(obj, "poster", "")

    def get_title(self, obj):
        return getattr(obj, "name", "")
