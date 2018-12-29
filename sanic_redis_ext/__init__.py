__version__ = '0.1.1'
__all__ = ['RedisExtension', ]

VERSION = __version__


from aioredis import create_redis_pool
from sanic_base_ext import BaseExtension


class RedisExtension(BaseExtension):
    extension_name = app_attribute = 'redis'

    def get_config(self, app):
        connection_uri = (
            self.get_from_app_config(app, 'REDIS_HOST'),
            self.get_from_app_config(app, 'REDIS_PORT'),
        )
        config = {
            "address": connection_uri,
            "db": self.get_from_app_config(app, 'REDIS_DATABASE', None),
            "password": self.get_from_app_config(app, 'REDIS_PASSWORD', None),
            "ssl": self.get_from_app_config(app, 'REDIS_SSL', None),
            "encoding": self.get_from_app_config(app, 'REDIS_ENCODING', None),
            "minsize": self.get_from_app_config(app, 'REDIS_MIN_SIZE_POOL', 1),
            "maxsize": self.get_from_app_config(app, 'REDIS_MAX_SIZE_POOL', 10),
        }
        return config

    def init_app(self, app, *args, **kwargs):
        super(RedisExtension, self).init_app(app, *args, **kwargs)

        @app.listener('before_server_start')
        async def aioredis_configure(app_inner, _loop):
            config = self.get_config(app_inner)
            aioredis_pool = await create_redis_pool(**config)

            setattr(app_inner, self.app_attribute, aioredis_pool)
            if not hasattr(app, 'extensions'):
                setattr(app, 'extensions', {})
            app.extensions[self.extension_name] = aioredis_pool

        @app.listener('after_server_stop')
        async def aioredis_free_resources(app_inner, _loop):
            aioredis_pool = getattr(app_inner, self.app_attribute, None)

            if aioredis_pool:
                aioredis_pool.close()
                await aioredis_pool.wait_closed()
