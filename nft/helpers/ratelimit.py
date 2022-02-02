import time

from patreon.services.caching import memcache


def _mc_key(user_id, action_name, limit, interval):
    # Round down to the nearest whole number interval.
    interval_start = int(time.time() / interval) * interval
    return ':'.join(['ratelimit', str(user_id), action_name, str(interval_start)])


def throttle(user_id, action_name, limit, interval):
    """Returns true if this function has been called with these parameters
    too many times."""
    key = _mc_key(user_id, action_name, limit, interval)
    # Determine if the user has too many actions since the interval_start.
    action_count = memcache.incr(key)
    if not action_count:
        memcache.set(key, 1)
        action_count = 1
    return action_count is not None and (action_count > limit)


def overlimit(user_id, action_name, limit, interval):
    """Determine if this user has gone over the limit without incrementing
    the rate count at the same time."""
    if not user_id:
        return False
    key = _mc_key(user_id, action_name, limit, interval)
    action_count = memcache.get(key)
    return action_count is not None and (action_count > limit)
