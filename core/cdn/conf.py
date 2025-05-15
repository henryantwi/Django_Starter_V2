from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")

# # R2 compatibility
# AWS_S3_REGION_NAME = "auto"
# AWS_S3_ADDRESSING_STYLE = "virtual"
# AWS_DEFAULT_ACL = None

# Optional: public-read for CDN access
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read",  # safe for public assets
}

# For STATIC_URL and MEDIA_URL
AWS_LOCATION = config("AWS_LOCATION")

STORAGES = {
    "default": {
        "BACKEND": "core.cdn.backends.MediaRootS3BotoStorage",
    },
    "staticfiles": {
        "BACKEND": "core.cdn.backends.StaticRootS3BotoStorage",
    },
}
