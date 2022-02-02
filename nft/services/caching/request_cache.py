import collections

import patreon
from patreon.util import function_tools

fallback_cache = None


class BaseCache(object):
    # TODO(postport): Implement kwargs as well.
    def __init__(self, inner_f):
        self.inner_f = inner_f
        self.f_prefix = inner_f.__module__ + '.' + inner_f.__name__

    def __call__(self, *args, **kwargs):
        """Pull the return value from the request cache if possible. If not,
        pull the return value from memcache if possible. If not, pull the
        value from calling inner_f, then set the value in request cache
        and memcache where needed."""
        key = self.mc_key_for(*args, **kwargs)

        # Get the value direct from request cache if it's there.
        request_cache = patreon.services.get_request_cache()
        if key in request_cache:
            return request_cache[key]
        else:
            key = self.mc_key_for(*args, **kwargs)
            result = self.inner_f(*args, **kwargs)
            request_cache[key] = result
            return result

    def mc_key_for(self, *args, **kwargs):
        # Convert args to kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        return ':'.join(
            [self.f_prefix] +
            [patreon.services.caching.arg_to_key(arg) for arg in args] +
            [patreon.services.caching.arg_to_key(key + str(arg)) for key, arg in sorted(kwargs.items())]
        )

    def delete(self, *args):
        """Remove the key from the request cache and from memcache."""
        request_cache = patreon.services.get_request_cache()
        key = self.mc_key_for(*args)
        if key in request_cache:
            del request_cache[key]


class MultigetCache(BaseCache):
    def __init__(self, inner_f, object_key, argument_key, default_result,
                 result_key, object_tuple_key):
        self.argument_tuple_list = []
        self.kwargs_dict = collections.defaultdict(list)
        self.object_key = object_key
        self.result_key = result_key
        self.default_result = default_result
        self.object_tuple_key = object_tuple_key

        # backwards compatibility
        self.multiget = True

        self.argument_key = argument_key
        if not argument_key:
            self.argument_key = function_tools.get_kwargs_for_function(inner_f)
        super(MultigetCache, self).__init__(inner_f)

    def __call__(self, *args, **kwargs):
        """
        Pull the return value from the request cache if possible. If not,
        pull the value from calling inner_f, then set the value in request cache
        """
        key = self.mc_key_for(*args, **kwargs)

        # Get the value direct from request cache if it's there.
        request_cache = patreon.services.get_request_cache()
        if key in request_cache:
            return request_cache[key]
        else:
            self.prime(*args, **kwargs)
            self._issue_gets_for_primes()
            return request_cache[key]

    def prime(self, *args, **kwargs):

        # Convert positional arguments into kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        # Used to calculate cache keys
        self.argument_tuple_list.append((args, kwargs.copy()))

        # Verify argument count (very light measure)
        if len(kwargs) != function_tools.get_arg_count(self.inner_f):
            raise Exception(
                'Invalid multiget args: ' + str(kwargs) + ' for function '
                + str(self.inner_f)
            )

        # Create parallel lists for each kwarg for each object added to the queue
        for key, value in kwargs.items():
            # sometimes we get a list??
            if hasattr(value, 'append'):
                value = value[0]
            self.kwargs_dict[key].append(str(value))

    def _issue_gets_for_primes(self):
        request_cache = patreon.services.get_request_cache()

        # Only call with kwargs because we converted earlier
        objects = self.inner_f(**self.kwargs_dict)
        # For the objects that were returned, reorder them such that they match
        # the order they were primed in, and if nothing was returned for a set
        # of arguments, use the provided default value
        mapped_objects = function_tools.map_arguments_to_objects(
            self.kwargs_dict, objects, self.object_key, self.object_tuple_key,
            self.argument_key, self.result_key, self.default_result
        )
        for (args, kwargs), mapped_object in zip(self.argument_tuple_list, mapped_objects):
            key = self.mc_key_for(*args, **kwargs)
            request_cache[key] = mapped_object

        # Reset
        self.argument_tuple_list = []
        self.kwargs_dict = collections.defaultdict(list)


def request_cached():
    def create_wrapper(inner_f):
        return BaseCache(inner_f)

    return create_wrapper


def multiget_cached(object_key, argument_key=None, default_result=None,
                    result_fields=None, join_table_name=None):
    def create_wrapper(inner_f):
        return MultigetCache(
            inner_f, object_key, argument_key, default_result, result_fields,
            join_table_name
        )

    return create_wrapper
