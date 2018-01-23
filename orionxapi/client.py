from pygql import Client
import ujson
import concurrent.futures
from .transport import CustomBatchTransport, CustomSessionTransport


def client(api_key, secret_key, use_batching=False, timeout=None, **kwargs):
  url = 'https://api2.orionx.io/graphql'
  if use_batching:
    cs = CustomBatchTransport(
      api_key,
      secret_key,
      url=url,
      use_json=True,
      timeout=timeout
    )
  else:
    cs = CustomSessionTransport(
      api_key,
      secret_key,
      url=url,
      use_json=True,
      timeout=timeout
    )
  client = Client(
    transport=cs,
    fetch_schema_from_transport=True,
    **kwargs
  )
  return client


def as_completed(exec_results, timeout=None):
  future_to_exres = {e.future: e for e in exec_results}
  for future in concurrent.futures.as_completed(future_to_exres, timeout):
    exec_result = future_to_exres[future]
    yield exec_result


if __name__ == '__main__':
  pass
