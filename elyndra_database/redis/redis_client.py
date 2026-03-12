import redis

from environment import REDIS_USER, REDIS_PASSWORD

CACHE_TTL = 300  # 5 minutos

r = redis.Redis(
    host='redis-15872.c265.us-east-1-2.ec2.cloud.redislabs.com',
    port=15872,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASSWORD
)