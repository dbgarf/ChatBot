import redis 
import os

def get_redis_client(host='localhost', port=6379, db=0):
    if os.getenv('CHATBOT_ENV') == 'test':
        return redis.Redis(host='localhost', port=6379, db=1)
    else:
        return redis.Redis(host=host, port=port, db=db)