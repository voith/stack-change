from toolz import dissoc


def get_or_create(model, data, constraint_keys):
    other_keys = set(data.keys()) - set(constraint_keys)
    default_dict = dissoc(data, *constraint_keys)
    constraint_dict = dissoc(data, *other_keys)
    return model.objects.get_or_create(defaults=default_dict, **constraint_dict)
