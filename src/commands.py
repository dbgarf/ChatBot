from src.world_time_api import WorldTimeAPI
from src.redis_client import get_redis_client

def timeat(timezone):
    api = WorldTimeAPI()
    result, message = api.get_time_at_timezone(timezone)

    if result:
        r = get_redis_client()
        count = r.get(timezone)
        if count is None:
            r.set(timezone, 1)
        else:
            r.set(timezone, int(count) + 1)
    return message

def timepopularity(timezone):
    r = get_redis_client()
    count = r.get(timezone)
    if count is None:
        return 0
    return count