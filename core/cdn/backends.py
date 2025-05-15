from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticRootS3BotoStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False

    def url(self, name: str) -> str:
        return f"{settings.AWS_LOCATION}/static/{name}"


class MediaRootS3BotoStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False

    def url(self, name: str) -> str:
        return f"{settings.AWS_LOCATION}/media/{name}"
