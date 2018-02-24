sanic-redis-extension
#####################
Redis support for Sanic framework

Features
========
- Based on the aioredis_ library
- Easy to use and configurate for your own projects

Installation
============
This package should be installed using pip: ::

    pip install sanic-redis-extension

Example
=======
.. code-block:: python

    from sanic import Sanic, response
    from sanic_redis_ext import RedisExtension

    app = Sanic(__name__)
    # Configuration for Redis
    app.config.update({
        "REDIS_HOST": "127.0.0.1"
        "REDIS_PORT": 6379
        "REDIS_DATABASE": None
        "REDIS_SSL": None
        "REDIS_ENCODING": None
        "REDIS_MIN_SIZE_POOL": 1
        "REDIS_MAX_SIZE_POOL": 10
    })
    RedisExtension(app) # Connection pool is available as `app.redis` or `app.extensions['redis']`

    @app.route("/")
    async def handle(request):
        with await request.app.redis as redis:
            await redis.set('test-my-key', 'value')
            val = await redis.get('test-my-key')
        return response.text(val.decode('utf-8'))

License
=======
The sanic-redis-extension is published under BSD license. For more details read LICENSE_ file.

.. _links:
.. _aioredis: http://aioredis.readthedocs.io/
.. _LICENSE: https://github.com/Relrin/sanic-redis-extension/blob/master/LICENSE
