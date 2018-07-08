
def save_profile(backend, user, response, *args, **kwargs):
    """Associate a Profile with a User."""
    if backend.name == 'stackoverflow':
        handle = user.username
