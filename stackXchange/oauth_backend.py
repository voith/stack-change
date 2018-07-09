from social_core.backends.stackoverflow import StackoverflowOAuth2
from social_core.utils import handle_http_errors


class StackoverflowOAuth2V2(StackoverflowOAuth2):

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        data = self.user_data(access_token, *args, **kwargs)
        response = kwargs.get('response') or {}
        response.update(data or {})
        if 'access_token' not in response:
            response['access_token'] = access_token
        kwargs.update({'response': response, 'backend': self})
        user_fields = self.setting('USER_FIELDS', [])
        kwargs.update({
            field: response[field] for field in user_fields if field in response
        })
        return self.strategy.authenticate(*args, **kwargs)
