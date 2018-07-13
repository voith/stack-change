from functools import partial

from toolz import merge

from app.models import User, UserAssociation, StackExchangeSite
from stackXchange.utils.functional import split_dict_by_keys
from stackXchange.utils.orm import get_or_create
from stackXchange.utils.stack_overflow_aouth import StackOverflowOauth


def save_user_profile(username):
    # TODO: run this task asyncronously
    api = StackOverflowOauth()
    user = User.objects.get(username=username)
    account_id = user.account_id
    user_data = api.get_user_from_account_id(account_id)
    site_data, user_data = split_dict_by_keys(user_data, {'domain', 'name'})
    site = get_or_create(StackExchangeSite, site_data, {'doamin'})
    data_to_inject = {'user_id': user.id, 'site_id': site.id}
    modified_user_data = map(partial(merge, data_to_inject), user_data)
    constraint_keys = {'site_name', 'site_user_id'}
    for _user in modified_user_data:
        get_or_create(UserAssociation, _user, constraint_keys)


def save_profile(backend, user, response, *args, **kwargs):
    """Associate a Profile with a User."""
    if backend.name == 'stackoverflow':
        save_user_profile(user.username)
