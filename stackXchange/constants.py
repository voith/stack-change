from urllib.parse import urljoin

STACK_EXCHANGE_OAUTH_BASE_URI = 'https://stackoverflow.com/'

# STACK_EXCHANGE_OAUTH_URI = urljoin(STACK_EXCHANGE_OAUTH_BASE_URI, 'oauth')

STACK_EXCHANGE_ACCESS_TOKEN_URI = urljoin(STACK_EXCHANGE_OAUTH_BASE_URI, 'oauth/access_token')

STACK_EXCHANGE_API_VERSION = '2.2'

STACK_EXCHANGE_API_BASE_URI = urljoin('https://api.stackexchange.com/', STACK_EXCHANGE_API_VERSION)

STACK_EXCHANGE_API_USER_ACESS_TOKEN = urljoin(STACK_EXCHANGE_API_BASE_URI, 'access-tokens/{access_token}')

STACK_EXCHANGE_API_USER_ASSOCCIATION = urljoin(STACK_EXCHANGE_API_BASE_URI, 'users/{user_id}/associated')

STACK_EXCHANGE_API_SITES = urljoin(STACK_EXCHANGE_API_BASE_URI, 'sites')

STACK_EXCHANGE_API_QUESTiON_DETAILS = urljoin(STACK_EXCHANGE_API_BASE_URI, 'questions/{question_id}')

STACK_EXCHANGE_API_QUESTiON_ANSWERS = urljoin(STACK_EXCHANGE_API_BASE_URI, 'questions/{question_id}/answers')
