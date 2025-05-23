from .base_config import BaseConfig


class Config(BaseConfig):
    SPINE_URL = ''
    SPINE_ACCESS_TOKEN = ''

    CDN_UPLOAD_URL = ''
    MYSTERY_VIDEO_API_URL = ''
    MYSTERY_VIDEO_ACCESS_TOKEN = ''

    CDN_ACCESS_TOKEN = ''


config = Config()
