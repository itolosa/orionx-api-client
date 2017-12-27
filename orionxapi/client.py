import requests
from orionxapi import queries as orionx_queries
import ujson

def async_query_wrapper(qfx):
  def query_builder_wrapper(self, *args, **kwargs):
    def deco_wrapper(*args2, **kwargs2):
      if self.registerable_queries:
        self.reg_keys.append(args[0])
        r = self.reg_queries.append(qfx(self, *args, **kwargs)(*args2, **kwargs2))
        return r
      else:
        try:
          self.reg_keys.append(args[0])
          r = self.execute_query(qfx(self, *args, **kwargs)(*args2, **kwargs2))
          self.clear_registry()
          return r
        except requests.exceptions.Timeout:
          self.clear_registry()
          print("Endpoint unreachable!")
          raise requests.exceptions.Timeout
      return None
    return deco_wrapper
  return query_builder_wrapper

def sync_query_wrapper(qfx):
  def query_builder_wrapper(self, *args, **kwargs):
    def deco_wrapper(*args2, **kwargs2):
      try:
        self.reg_keys.append(args[0])
        r = self.bulk_query([qfx(self, *args, **kwargs)(*args2, **kwargs2)], use_naming=False)[0]
        self.clear_registry()
        return r
      except requests.exceptions.Timeout:
        self.clear_registry()
        print("Endpoint unreachable!")
        raise requests.exceptions.Timeout
      return None
    return deco_wrapper
  return query_builder_wrapper

class OrionxApiClient(object):
  def __init__(self, additional_headers={}, registerable=True):
    self.session_headers = {
      'authority': 'api.orionx.io',
      'dnt': '1',
      'referer': 'https://orionx.io/exchange/CHACLP',
      'cache-control': 'no-cache',
      'accept': '*/*',
      'content-type': 'application/json',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'pragma': 'no-cache',
      'accept-language': 'en-US,en;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'origin': 'https://orionx.io'
    }

    self.api_url = 'https://api.orionx.io/graphql'
    self.session = requests.Session()
    self.session_headers.update(additional_headers)
    self.session.headers.update(self.session_headers)
    self.registerable_queries = registerable
    self.reg_queries = []
    self.reg_keys = []
    self.retry_limit = 3

    self.requests_timeout = 5

  def clear_registry(self):
    self.reg_keys = []
    self.reg_queries = []

  def name_results(self, results):
    return dict(zip(self.reg_keys, results))

  def process_result(self, result):
    return ujson.loads(result.text)

  def send_queries(self, queries):
    retries_count = 0
    while True:
      try:
        r = self.session.post(url=self.api_url, json=queries, timeout=self.requests_timeout)
        return self.process_result(r)
      except requests.exceptions.Timeout:
        if retries_count > self.retry_limit:
          raise requests.exceptions.Timeout
        retries_count += 1
    return None

  def bulk_query(self, queries, parallel=True, use_naming=True):
    results = []
    if parallel:
      results = self.send_queries(queries)
    else:
      for query in queries:
        results.append(self.send_queries([query])[0])
    if use_naming:
      return self.name_results(results)
    return results

  @sync_query_wrapper
  def execute_query(self, query_name):
    return getattr(orionx_queries, query_name)

  @async_query_wrapper
  def register_query(self, query_name):
    return getattr(orionx_queries, query_name)

  def perform_queries(self):
    if self.registerable_queries:
      try:
        results = self.bulk_query(self.reg_queries)
        self.clear_registry()
        return results
      except requests.exceptions.Timeout:
        try:
          results = self.bulk_query(self.reg_queries, parallel=False)
          self.clear_registry()
          return results
        except requests.exceptions.Timeout:
          self.clear_registry()
          print("Endpoint unreachable!")
          raise requests.exceptions.Timeout
      return None
    return None

if __name__ == '__main__':
  orionx = OrionxApiClient()
  orionx.register_query('getMe')()
  orionx.register_query('getOrderBook')()
  print(orionx.perform_queries())
