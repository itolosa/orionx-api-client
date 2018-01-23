import ujson
import requests
import hmac
import time
from hashlib import sha512
from pygql.transport.batch_transport import BatchTransport
from pygql.transport.session_transport import SessionTransport
from graphql.language.printer import print_ast
from graphql.execution import ExecutionResult

def hmac_sha512(secret_key, timestamp, body):
  key = bytearray(secret_key, 'utf-8')
  msg = str(timestamp) + str(body)
  msg = msg.encode('utf-8')
  return hmac.HMAC(key, msg, sha512).hexdigest()


class CustomBatchTransport(BatchTransport):
  def __init__(self, api_key, secret_key, *args, **kwargs):
    super(CustomBatchTransport, self).__init__(*args, **kwargs)
    self.api_key = api_key
    self.secret_key = secret_key

  def _batch_query(self):
    while self.query_batcher_active:
      query_payloads = []
      futures = []
      payload, future = self.query_batcher_queue.get()

      if not self.query_batcher_active:
        break
      query_payloads.append(payload)
      futures.append(future)
      # wait 10 ms
      time.sleep(0.01)
      while not self.query_batcher_queue.empty():
        if not self.query_batcher_active:
          break
        payload, future = self.query_batcher_queue.get()
        query_payloads.append(payload)
        futures.append(future)

      new_futures = []
      new_query_payloads = []
      for payload, future in zip(query_payloads, futures):

        if future.set_running_or_notify_cancel():
          new_futures.append(future)
          new_query_payloads.append(payload)

      try:
        data = ujson.dumps(new_query_payloads)
        timestamp = str(time.time())
        signature = str(hmac_sha512(self.secret_key, timestamp, data))

        headers = {
          'Content-Type': 'application/json',
          'X-ORIONX-TIMESTAMP': timestamp,
          'X-ORIONX-APIKEY': self.api_key,
          'X-ORIONX-SIGNATURE': signature
        }

        post_args = {
          'timeout': self.timeout,
          'data': data,
          'headers': headers
        }

        request = self.session.post(self.url, **post_args)
        request.raise_for_status()
        results = request.json()
        for result, future in zip(results, new_futures):
          try:
            assert 'errors' in result or 'data' in result, \
                'Received non-compatible response "{}"'.format(result)
            future.set_result(result)
          except Exception as exc:
            future.set_exception(exc)
      except Exception as exc:
        for future in new_futures:
          future.set_exception(exc)


class CustomSessionTransport(SessionTransport):
  def __init__(self, api_key, secret_key, *args, **kwargs):
    super(CustomSessionTransport, self).__init__(*args, **kwargs)
    self.api_key = api_key
    self.secret_key = secret_key

  def execute(self, document, variable_values=None, timeout=None):
    query_str = print_ast(document)
    payload = {
      'query': query_str,
      'variables': variable_values or {}
    }

    timestamp = str(time.time())
    data = ujson.dumps(payload)
    signature = str(hmac_sha512(self.secret_key, timestamp, data))

    headers = {
      'Content-Type': 'application/json',
      'X-ORIONX-TIMESTAMP': timestamp,
      'X-ORIONX-APIKEY': self.api_key,
      'X-ORIONX-SIGNATURE': signature
    }

    post_args = {
      'timeout': timeout or self.default_timeout,
      'data': data,
      'headers': headers
    }
    
    request = self.session.post(self.url, **post_args)
    request.raise_for_status()

    result = request.json()
    assert 'errors' in result or 'data' in result, 'Received non-compatible response "{}"'.format(result)
    return ExecutionResult(
      errors=result.get('errors'),
      data=result.get('data')
    )
