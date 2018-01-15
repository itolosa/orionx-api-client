from pygql import Client
import ujson
import hashlib
import concurrent.futures
from .transport import CustomBatchTransport, CustomSessionTransport


def client(api_key, secret_key, use_batching=False):
  url = 'https://api.orionx.io/graphql'
  if use_batching:
    cs = CustomBatchTransport(
      url=url,
      api_key,
      secret_key,
      use_json=True,
      timeout=5
    )
  else:
    cs = CustomSessionTransport(
      url=url,
      api_key,
      secret_key,
      use_json=True,
      timeout=5
    )
  client = Client(
    retries=3,
    transport=cs,
    fetch_schema_from_transport=True
  )
  return client


def as_completed(exec_results, timeout=None):
  future_to_exres = {e.future: e for e in exec_results}
  for future in concurrent.futures.as_completed(future_to_exres, timeout):
    exec_result = future_to_exres[future]
    yield exec_result


if __name__ == '__main__':
  pass
