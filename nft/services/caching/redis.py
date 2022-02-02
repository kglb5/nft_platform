"""
services/redis.py

In memory key-value cache with LRU-based evictions.
"""
from hashlib import sha256
import functools
import memcache

import patreon
from patreon.util import function_tools
from patreon.util.unsorted import jsdecode, jsencode, get_utf8_string

_cache = None


def initialize():
    global _cache
    servers = patreon.config.memcached['servers']
    _cache = memcache.Client(servers=servers)


def get(key):
    # TODO(postport): Possibly move away from this and automatically JSON encode.
    return _cache.get(key)


def get_multi(keys):
    # TODO(port)
    pass


def set(key, value, expires_seconds=0):
    # TODO(postport): Possibly move away from this and automatically JSON encode.
    return _cache.set(key, value, time=expires_seconds)


def set_multi(key_value_pairs):
    # TODO(port)
    pass


def delete(key):
    _cache.delete(key)
    # TODO(postport): This is a hack to make sure that mc.deletes also delete
    # any incidental cached python versions of keys. This is only important
    # for mc.deletes that are straight ported from PHP.
    if not key.startswith('py'):
        _cache.delete('py:' + key)


def incr(key):
    return _cache.incr(key)


def flush_all():
    return _cache.flush_all()


class Memcached:
    def __init__(self, inner_f, time_to_cache):
        self.inner_f = inner_f
        self.f_prefix = inner_f.__module__ + '.' + inner_f.__name__
        self.time_to_cache = time_to_cache

    def __call__(self, *args, **kwargs):
        if _cache is None:
            return self.inner_f(*args, **kwargs)

        key = self.mc_key_for(*args, **kwargs)
        value = get(key)
        if value and jsdecode(value):
            return jsdecode(value)

        result = self.inner_f(*args, **kwargs)
        try:
            set(key=key, value=jsencode(result), expires_seconds=self.time_to_cache)
        except:
            pass
        return result

    def mc_key_for(self, *args, **kwargs):
        # Convert args to kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        plaintext_key = ':'.join(
            [patreon.config.main_server] +
            [self.f_prefix] +
            [patreon.services.caching.arg_to_key(arg) for arg in args] +
            [patreon.services.caching.arg_to_key(key + str(arg)) for key, arg in sorted(kwargs.items())]
        )

        return sha256(get_utf8_string(plaintext_key)).hexdigest()

    def delete(self, *args, **kwargs):
        if _cache is None:
            return None
        key = self.mc_key_for(*args, **kwargs)
        delete(key)


def memcached(time_to_cache=600):
    def create_wrapper(inner_f):
        return functools.update_wrapper(
            Memcached(inner_f, time_to_cache),
            inner_f
        )

    return create_wrapper
