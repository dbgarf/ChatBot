from src.world_time_api import WorldTimeAPI
import redis 

def timeat(timezone):
    api = WorldTimeAPI()
    result, message = api.get_time_at_timezone(timezone)

    if result:
        r = redis.Redis(host='localhost', port=6379, db=0)
        count = r.get(timezone)
        if count is None:
            r.set(timezone, 1)
        else:
            r.set(timezone, int(count) + 1)
    return message

def timepopularity(timezone):
    r = redis.Redis(host='localhost', port=6379, db=0)
    count = r.get(timezone)
    if count is None:
        return 0
    return count