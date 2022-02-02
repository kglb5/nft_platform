import base64

from .request_cache import request_cached
from .request_cache import multiget_cached
from .redis import memcached
from . import redis
from .jinja_bytecode_cache import MemoryBytecodeCache

def arg_to_key(arg):
    if isinstance(arg, int):
        return str(arg)
    elif isinstance(arg, str):
        return base64.b64encode(bytearray(arg, "utf-8")).decode('utf-8')
    elif isinstance(arg, list):
        return ','.join([arg_to_key(inner_arg) for inner_arg in arg])
    elif arg is None:
        # Unlikely to collide with base64 encoded string above
        return 'value:none'
    else:
        print('trying to get a key for', str(arg))
        raise NotImplemented()
