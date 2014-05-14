import os

from django.conf import settings

MODULE_ROOT = os.path.dirname(os.path.realpath(__file__))


def pytest_configure():

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        USE_TZ=True,
        INSTALLED_APPS=(
            "zencoder",
        ),
        ROOT_URLCONF = "testproject.urls",
        VIDEO_ENCODING_DIRECTORY = "video",
        VIDEO_ENCODING_BUCKET = "example_bucket",

        AWS_SECRET_ACCESS_KEY = "12345",
        AWS_ACCESS_KEY_ID = "abcd1234",
    )
