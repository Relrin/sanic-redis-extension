__version__ = '0.2.0'
__all__ = ['RedisExtension', ]

VERSION = __version__


from sanic_base_ext import BaseExtension
from redis.asyncio import Redis


class RedisExtension(BaseExtension):
    extension_name = app_attribute = 'redis'

    def get_config(self, app):
        config = {
            'host': self.get_from_app_config(app, 'REDIS_HOST', 'localhost'),
            'port': self.get_from_app_config(app, 'REDIS_PORT', 6379),
            'db': self.get_from_app_config(app, 'REDIS_DATABASE', 0),
            'username': self.get_from_app_config(app, 'REDIS_USERNAME', None),
            'password': self.get_from_app_config(app, 'REDIS_PASSWORD', None),
            'socket_timeout': self.get_from_app_config(app, 'REDIS_SOCKET_TIMEOUT', None),
            'socket_connect_timeout': self.get_from_app_config(app, 'REDIS_SOCKET_CONNECT_TIMEOUT', None),
            'socket_keepalive': self.get_from_app_config(app, 'REDIS_SOCKET_KEEP_ALIVE', None),

            'ssl': self.get_from_app_config(app, 'REDIS_SSL', False),
            'ssl_keyfile': self.get_from_app_config(app, 'REDIS_SSL_KEYFILE', None),
            'ssl_certfile': self.get_from_app_config(app, 'REDIS_SSL_CERTFILE', None),
            'ssl_cert_reqs': self.get_from_app_config(app, 'REDIS_SSL_CERT_REQS', "required"),
            'ssl_ca_certs': self.get_from_app_config(app, 'REDIS_SSL_CA_CERTS', None),
            'ssl_ca_data': self.get_from_app_config(app, 'REDIS_SSL_CA_DATA', None),
            'ssl_check_hostname': self.get_from_app_config(app, 'REDIS_SSL_CHECK_HOSTNAME', False),

            'encoding': self.get_from_app_config(app, 'REDIS_ENCODING', 'utf-8'),
            'retry_on_timeout':  self.get_from_app_config(app, 'REDIS_RETRY_ON_TIMEOUT', False),
            'max_connections': self.get_from_app_config(app, 'REDIS_MAX_CONNECTIONS', 10),
            'health_check_interval': self.get_from_app_config(app, 'REDIS_HEALTH_CHECK_INTERVAL', 0),
            'auto_close_connection_pool': self.get_from_app_config(app, 'REDIS_AUTO_CLOSE_CONNECTION_POOL', True),
        }
        return config

    def init_app(self, app, *args, **kwargs):
        super(RedisExtension, self).init_app(app, *args, **kwargs)

        @app.listener('before_server_start')
        async def aioredis_configure(app_inner, _loop):
            config = self.get_config(app_inner)
            redis_client = Redis(**config)

            setattr(app_inner.ctx, self.app_attribute, redis_client)
            if not hasattr(app.ctx, 'extensions'):
                setattr(app.ctx, 'extensions', {})

            app.ctx.extensions[self.extension_name] = redis_client

        @app.listener('after_server_stop')
        async def aioredis_free_resources(app_inner, _loop):
            redis_client = getattr(app_inner.ctx, self.app_attribute, None)

            if redis_client:
                await redis_client.close()
