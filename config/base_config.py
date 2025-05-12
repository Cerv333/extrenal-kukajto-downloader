class BaseConfig:
    SPINE_URL = ''
    SPINE_ACCESS_TOKEN = ''

    CDN_UPLOAD_URL = ''
    MYSTERY_VIDEO_API_URL = ''
    MYSTERY_VIDEO_ACCESS_TOKEN = ''

    def get(self, key: str, default: any = None) -> any:
        return getattr(self, key, default)
