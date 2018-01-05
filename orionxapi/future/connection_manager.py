from gql import gql, Client
import getpass
import ujson
from gql.transport.requests import RequestsHTTPTransport
import requests
from fake_useragent import UserAgent
import hashlib
import datetime
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast
from .future.dsl import DSLSchema

def valid_token(expirets):
  delta_t = (datetime.datetime.fromtimestamp(expirets/1000.0) - datetime.datetime.now())
  return datetime.timedelta(days=1) < delta_t

def login_gen(email, password):
  m = hashlib.sha256()
  m.update(password.encode('ascii'))
  pass_digest = m.hexdigest()
  digest_alg = 'sha-256'
  return [{
    "query": "mutation login($username: String, $email: String, $password: HashedPassword!) {\n  loginWithPassword(username: $username, email: $email, password: $password) {\n    id\n    token\n    tokenExpires\n    __typename\n  }\n}\n",
    "variables": {
      "email": email,
      "password": {
        "digest": pass_digest,
        "algorithm": digest_alg
      }
    },
    "operationName": "login"
  }]

def authorize_gen(code):
  return [{
    "query": "mutation authorizeSession($code: String) {\n  authorizeSession(code: $code) {\n    success\n    __typename\n  }\n}\n",
    "variables": {
      "code": code
    },
    "operationName": "authorizeSession"
  }]


class CustomTransport(RequestsHTTPTransport):
  def __init__(self, url, cookies, **kwargs):
    """
    :param url: The GraphQL URL
    :param auth: Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth
    :param use_json: Send request body as JSON instead of form-urlencoded
    :param timeout: Specifies a default timeout for requests (Default: None)
    """
    super(CustomTransport, self).__init__(url, **kwargs)
    self.session = requests.Session()
    self.cookies = cookies
    self.session.cookies = requests.utils.cookiejar_from_dict(self.cookies)
    self.session.headers.update(self.headers)
    self.session.auth = self.auth

  def execute(self, document, variable_values=None, timeout=None):
    query_str = print_ast(document)
    payload = {
      'query': query_str,
      'variables': variable_values or {}
    }

    data_key = 'json' if self.use_json else 'data'
    post_args = {
      'timeout': timeout or self.default_timeout,
      data_key: payload
    }
    request = self.session.post(self.url, **post_args)
    request.raise_for_status()

    result = request.json()
    assert 'errors' in result or 'data' in result, 'Received non-compatible response "{}"'.format(result)
    return ExecutionResult(
      errors=result.get('errors'),
      data=result.get('data')
    )

def client():

  login_url = ''
  endpoint_url = 'https://api.orionx.io/graphql'
  cache_exists = True

  try:
    headers_cachefp = open('headers_cache.json', 'r')
    headers_tuple = ujson.load(headers_cachefp)
    headers_cachefp.close()
  except FileNotFoundError:
    cache_exists = False

  if cache_exists and valid_token(headers_tuple[1]):
    cookies_cachefp = open('cookies_cache.json', 'r')
    cookies = ujson.load(cookies_cachefp)
    cookies_cachefp.close()
    headers = headers_tuple[0]
  else:
    # get user agent via fake_useragent
    print('Obtaining a fake user agent from useragentstring.com ...')
    ua = UserAgent()
    user_agent = ua.random
    print('Done.')
    custom_headers = {
      "accept": "*/*",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "en-US,en;q=0.9",
      "cache-control": "no-cache",
      "dnt": "1",
      "origin": "https://orionx.io",
      "pragma": "no-cache",
      "user-agent": user_agent
    }
    sess = requests.Session()
    sess.headers.update(custom_headers)

    request = sess.get('https://orionx.io/')
    request.raise_for_status()

    request = sess.get('https://orionx.io/login')
    request.raise_for_status()

    login_success = False
    while not login_success:
      print('Logging in ...')
      request = sess.post('https://api.orionx.io/graphql', json=login_gen(input('User: '), getpass.getpass()))
      request.raise_for_status()

      login_info = ujson.loads(request.text)
      if 'errors' in login_info[0]:
        for err in login_info[0]['errors']:
          print('ERROR:', err['message'])
        login_success = False
      else:
        login_success = True

    login_token = login_info[0]['data']['loginWithPassword']['token']
    token_expires = login_info[0]['data']['loginWithPassword']['tokenExpires']
    sess.headers.update({'login-token': login_token})

    authorize_success = False
    while not authorize_success:
      request = sess.post('https://api.orionx.io/graphql', json=authorize_gen(input('Verification Code: ')))
      request.raise_for_status()

      login_info = ujson.loads(request.text)
      if 'errors' in login_info[0]:
        for err in login_info[0]['errors']:
          print('ERROR:', err['message'])
        authorize_success = False
      else:
        authorize_success = True

    print('OK.')

    headers_cachefp = open('headers_cache.json', 'w')
    cookies_cachefp = open('cookies_cache.json', 'w')
    headers_cachefp.write(ujson.dumps([dict(sess.headers), token_expires]))
    cookies_cachefp.write(ujson.dumps(requests.utils.dict_from_cookiejar(request.cookies)))
    headers_cachefp.close()
    cookies_cachefp.close()
    
    cookies = requests.utils.dict_from_cookiejar(sess.cookies)
    headers = sess.headers

  return Client(retries=3, transport=CustomTransport(url=endpoint_url, use_json=True, timeout=5,
                headers=headers, cookies=cookies),
                fetch_schema_from_transport=True)

def cgql(document):
  return gql('{%s}' % document)

client = client()
ds = DSLSchema(client)
query_dsl = ds.Query.marketStats.args(marketCode="CHACLP", aggregation="h1").select(ds.MarketStatsPoint.open)
print(ds.execute(cgql(query_dsl)))
