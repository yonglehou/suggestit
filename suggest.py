"""
Simple search suggestions interface powered by redis and web.py
"""

import web
import redis
import json
from werkzeug.contrib.cache import MemcachedCache


# SETTINGS
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
MEMCACHE_ADDRESS = '127.0.0.1:11211'
CACHE_DURATION = 86400 # To prevent the redis server being hammered with gets, this stores the json result
ALLOW_THIRD_PARTY_ACCESS = False # Set this to true if you are accessing suggestions from a different domain name via Javascript

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
cache = MemcachedCache([MEMCACHE_ADDRESS])

urls = (
  '/suggestit/','home',
  '/suggestit/set/(.*)', 'set',
  '/suggestit/get/', 'get',
)


app = web.application(urls, globals())

class home:
    def GET(self):
        return 'Suggestit search suggestion engine'

class set:
    """
    Sets or increments search suggestions. 
    We break down the search query into different sorted sets as follows. eg. super mario 64
    s*, super mario 64, 1
    su*, super mario 64, 1
    ....
    super mario 64, super mario 64, 1
    
    If the set already has the element we have here, simply increment it's hit count
    This is just an example interface for setting keys. In practice, *NEVER* set
    database elements using a GET request.
    """
    def GET(self,name):
        name = name.lower()

        for i in range(1,len(name)+1):
            set_name = name[0:i] + ':star'
            r.zincrby(set_name,name,1.0)
        return name

if __name__ == "__main__": app.run()

class get:
    def GET(self):
        name = web.input(term = 'super mario')
        result_list = []
        set_name = name['term'].lower()+':star'
        results = r.zrevrange(set_name,0,10)
        if ALLOW_THIRD_PARTY_ACCESS:
            web.header('Access-Control-Allow-Origin','*')        
        if 'term' in web.input():
            key = 'sug:'+web.url()+'?term='+web.input()['term']
            key = key.replace(' ','+')
            cache.set(key, json.dumps(results), CACHE_DURATION)
        return json.dumps(results)

application = app.wsgifunc()