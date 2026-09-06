import json

import redis

from config import Config

redis_client = redis.Redis.from_url(Config.CELERY_BROKER_URL, decode_responses=True)

TREK_CACHE_TTL = 60


def cache_get(key):
    val = redis_client.get(key)
    return json.loads(val) if val else None


def cache_set(key, value, ttl=TREK_CACHE_TTL):
    redis_client.setex(key, ttl, json.dumps(value))


def cache_invalidate(prefix):
    keys = redis_client.keys(f"{prefix}*")
    if keys:
        redis_client.delete(*keys)
