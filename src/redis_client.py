import redis 

def get_redis_client(host='localhost', port=6379, db=0):
    r = redis.Redis(host=host, port=port, db=db)
    return r
