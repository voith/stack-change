import collections
import functools
import itertools

from toolz import (
    compose as _compose,
)
from toolz.dicttoolz import dissoc


def identity(value):
    return value


def combine(f, g):
    return lambda x: f(g(x))


def apply_to_return_value(callback):
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return callback(fn(*args, **kwargs))

        return inner
    return outer


to_tuple = apply_to_return_value(tuple)
to_list = apply_to_return_value(list)
to_dict = apply_to_return_value(dict)
to_ordered_dict = apply_to_return_value(collections.OrderedDict)
to_set = apply_to_return_value(set)
sort_return = _compose(to_tuple, apply_to_return_value(sorted))
flatten_return = _compose(to_tuple, apply_to_return_value(itertools.chain.from_iterable))
reversed_return = _compose(to_tuple, apply_to_return_value(reversed), to_tuple)


@to_dict
def apply_key_map(key_mappings, value):
    key_conflicts = set(
        value.keys()
    ).difference(
        key_mappings.keys()
    ).intersection(
        v
        for k, v
        in key_mappings.items()
        if v in value
    )
    if key_conflicts:
        raise KeyError(
            "Could not apply key map due to conflicting key(s): {}".format(key_conflicts)
        )

    for key, item in value.items():
        if key in key_mappings:
            yield key_mappings[key], item
        else:
            yield key, item


def split_dict_by_keys(_dict, keys):
    other_keys = set(_dict.keys()) - set(keys)
    dict2 = dissoc(_dict, *keys)
    dict1 = dissoc(_dict, *other_keys)
    return dict1, dict2


def dict_keep_only_keys(_dict, keys):
    other_keys = set(_dict.keys()) - set(keys)
    return dissoc(_dict, *other_keys)
