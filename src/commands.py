from src.world_time_api import WorldTimeAPI
from src.redis_client import get_redis_client

def timeat(tzinfo):
    api = WorldTimeAPI()
    result, message = api.get_time_at_timezone(tzinfo)

    if result:
        r = get_redis_client()
        count = r.get(tzinfo)
        if count is None:
            r.set(tzinfo, 1)
        else:
            r.set(tzinfo, int(count) + 1)
    return message

def timepopularity(tzinfo_or_prefix):
    """
    the argument here might be a prefix like America or America/Argentina
    so to get the count we want to scan the redis keys and sum the matches
    """

    r = get_redis_client()
    pattern = tzinfo_or_prefix + "*"
    # performance note: the KEYS command in redis runs in O(n) time where n is number of keys in the database
    # for large scale deployments this might become a performance issue, but probably not a big deal here
    # because the maximum size of the keyspace in this use case is only 386 (number of canonical timezones in worldtimeapi.org)
    matching_keys = r.keys(pattern)
    acc = 0
    for key in matching_keys:
        acc += int(r.get(key))
    return acc