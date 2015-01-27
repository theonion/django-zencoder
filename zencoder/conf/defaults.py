VIDEO_PREFERENCES = (
    "video/mp4",
    "video/webm",
    "application/x-mpegURL"
)

VIDEO_URL_PROCESSOR = None
VIDEO_ENCODING_MAX_SIZE = 1073741824
ZENCODER_API_KEY = None
ZENCODER_JOB_PAYLOAD = {
    "outputs": [
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
}
