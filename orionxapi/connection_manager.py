from gql import gql, Client
import getpass
import ujson
import requests
from fake_useragent import UserAgent
import hashlib
import datetime
from .lib.dsl import DSLSchema
from .lib.custom_transport import CustomTransport
from .client import OrionxApiClient

def valid_token(expirets):
  delta_t = (datetime.datetime.fromtimestamp(expirets/1000.0) - datetime.datetime.now())
  return datetime.timedelta(days=1) < delta_t

def digest_sha256(password):
  m = hashlib.sha256()
  m.update(password.encode('ascii'))
  pass_digest = m.hexdigest()
  return pass_digest

def client(headers_filename, cookies_filename):
  login_url = ''
  endpoint_url = 'https://api.orionx.io/graphql'
  cache_exists = True

  try:
    headers_cachefp = open(headers_filename, 'r')
    headers_tuple = ujson.load(headers_cachefp)
    headers_cachefp.close()
  except FileNotFoundError:
    cache_exists = False

  if cache_exists and valid_token(headers_tuple[1]):
    cookies_cachefp = open(cookies_filename, 'r')
    cookies = ujson.load(cookies_cachefp)
    cookies_cachefp.close()
    headers = headers_tuple[0]
    return Client(retries=3, transport=CustomTransport(url=endpoint_url, use_json=True, timeout=5,
                headers=headers, cookies=cookies),
                fetch_schema_from_transport=True)
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

    cs = CustomTransport(url=endpoint_url, use_json=True, timeout=5,
        headers=sess.headers, cookies=requests.utils.dict_from_cookiejar(sess.cookies))
    client = Client(retries=3, transport=cs,
        fetch_schema_from_transport=True)
    ds = DSLSchema(client)

    login_success = False
    while not login_success:
      try:
        user_email = input('User: ')
        pdigest = digest_sha256(getpass.getpass())
        result = ds.mutate(ds.Mutation.loginWithPassword.args(
          email=user_email,
          password={
            'digest': pdigest,
            'algorithm': 'sha-256'
          }).select(
          ds.LoginMethodResponse.token,
          ds.LoginMethodResponse.tokenExpires))
        login_success = True
      except (Exception, e):
        print('Error:', str(e))

    login_token = result['loginWithPassword']['token']
    token_expires = result['loginWithPassword']['tokenExpires']
    cs.session.headers.update({'login-token': login_token})

    authorize_success = False
    while not authorize_success:
      try:
        vcode = input('Verification Code: ')
        result = ds.mutate(ds.Mutation.authorizeSession.args(
          code=vcode).select(
          ds.AuthSuccessResponse.success))
        authorize_success = True
      except (Exception, e):
        print('Error:', str(e))

    print('Success:', result['authorizeSession']['success'])

    headers_cachefp = open(headers_filename, 'w')
    cookies_cachefp = open(cookies_filename, 'w')
    headers_cachefp.write(ujson.dumps([dict(cs.session.headers), token_expires]))
    cookies_cachefp.write(ujson.dumps(requests.utils.dict_from_cookiejar(cs.session.cookies)))
    headers_cachefp.close()
    cookies_cachefp.close()
    
    return client

def orionxapi_builder(headers_filename, cookies_filename):
  login_url = ''
  endpoint_url = 'https://api.orionx.io/graphql'
  cache_exists = True

  try:
    headers_cachefp = open(headers_filename, 'r')
    headers_tuple = ujson.load(headers_cachefp)
    headers_cachefp.close()
  except FileNotFoundError:
    cache_exists = False

  if cache_exists and valid_token(headers_tuple[1]):
    cookies_cachefp = open(cookies_filename, 'r')
    cookies = ujson.load(cookies_cachefp)
    cookies_cachefp.close()
    headers = headers_tuple[0]
    return OrionxApiClient(additional_headers=headers)
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

    cs = CustomTransport(url=endpoint_url, use_json=True, timeout=5,
        headers=sess.headers, cookies=requests.utils.dict_from_cookiejar(sess.cookies))
    client = Client(retries=3, transport=cs,
        fetch_schema_from_transport=True)
    ds = DSLSchema(client)

    login_success = False
    while not login_success:
      try:
        user_email = input('User: ')
        pdigest = digest_sha256(getpass.getpass())
        result = ds.mutate(ds.Mutation.loginWithPassword.args(
          email=user_email,
          password={
            'digest': pdigest,
            'algorithm': 'sha-256'
          }).select(
          ds.LoginMethodResponse.token,
          ds.LoginMethodResponse.tokenExpires))
        login_success = True
      except (Exception, e):
        print('Error:', str(e))

    login_token = result['loginWithPassword']['token']
    token_expires = result['loginWithPassword']['tokenExpires']
    cs.session.headers.update({'login-token': login_token})

    authorize_success = False
    while not authorize_success:
      try:
        vcode = input('Verification Code: ')
        result = ds.mutate(ds.Mutation.authorizeSession.args(
          code=vcode).select(
          ds.AuthSuccessResponse.success))
        authorize_success = True
      except (Exception, e):
        print('Error:', str(e))

    print('Success:', result['authorizeSession']['success'])

    headers_cachefp = open(headers_filename, 'w')
    cookies_cachefp = open(cookies_filename, 'w')
    headers_cachefp.write(ujson.dumps([dict(cs.session.headers), token_expires]))
    cookies_cachefp.write(ujson.dumps(requests.utils.dict_from_cookiejar(cs.session.cookies)))
    headers_cachefp.close()
    cookies_cachefp.close()
    
    return cs.session.OrionxApiClient(additional_headers=cs.session.headers, 
      cookies=requests.utils.dict_from_cookiejar(cs.session.cookies))

if __name__ == '__main__':
  client = client()
  ds = DSLSchema(client)
  query_dsl = ds.Query.marketStats.args(marketCode="CHACLP", aggregation="h1").select(ds.MarketStatsPoint.open)
  print(ds.execute(cgql(query_dsl)))
