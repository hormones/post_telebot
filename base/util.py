import json
import os
import cachetools

from base.types import MyJSONEncoder

# cache by ttl for 5 minutes
CACHE_TTL = cachetools.TTLCache(maxsize=9999, ttl=60)


def dumps(jsonobject):
    """
    json dumps with custom encoder, special util for object
    """
    return (
        json.dumps(jsonobject, cls=MyJSONEncoder)
        .replace("\\", "")
        .replace('"{', "{")
        .replace('}"', "}")
    )


def get_config(dic: dict, key: str, default=None):
    """
    get config value
    step 1: try to get value from env
    step 2: try to get value from config
    step 3: return default value
    """
    value = os.environ.get(key)
    if value is None:
        if key not in dic and default is None:
            raise ValueError(f"config key not found: {key}")
        value = dic.get(key, default)
    return value


def cache_ttl(key, value):
    CACHE_TTL[key] = value


def cache_ttl_get(key, default=None):
    return CACHE_TTL.get(key, default)


def cache_ttl_exists(key):
    return key in CACHE_TTL


def cache_ttl_if_absent(key, value):
    if cache_ttl_exists(key):
        return False
    cache_ttl(key, value)
    return True


def del_cache_ttl(key):
    CACHE_TTL.pop(key, None)


def clear_cache_ttl():
    CACHE_TTL.clear()
