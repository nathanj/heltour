DEBUG = True

INTERNAL_IPS = ['172.25.0.1']
LICHESS_DOMAIN = 'https://lichess.dev/'
API_WORKER_HOST = 'http://api:8880'
ALLOWED_HOSTS = ['localhost', 'api']

SLACK_API_TOKEN_FILE_PATH = './slack-token'
SLACK_WEBHOOK_FILE_PATH = './slack-webhook'
LICHESS_API_TOKEN_FILE_PATH = './lichess-token'

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': 'heltour_lichess4545',
        'USER': 'heltour_lichess4545',
        'PASSWORD': 'sown shuts combiner chattels',
    }
}

# redis
BROKER_URL = 'redis://redis:6379/1'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CACHEOPS_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 1,
}
