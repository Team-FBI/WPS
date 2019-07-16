from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):

    location = ''
    bucket_name = 'media.tthae.com'
    region_name = 'ap-northeast-2'
    custom_domain = bucket_name
    file_overwrite = False

