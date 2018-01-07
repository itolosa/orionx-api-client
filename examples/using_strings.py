from orionxapi.connection_manager import client
from orionxapi.lib.dsl import DSLSchema
from gql import gql
import hashlib
from getpass import getpass

def digest_sha256(password):
  m = hashlib.sha256()
  m.update(password.encode('ascii'))
  pass_digest = m.hexdigest()
  return pass_digest

# handler initialization with custom headers
client = client(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')

query = gql('''
  query getMarketStats($marketCode: ID!, $aggregation: MarketStatsAggregation!) {
    marketStats(marketCode: $marketCode, aggregation: $aggregation) {
      _id
      open
      close
      high
      low
      volume
      count
      fromDate
      toDate
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "aggregation": "h1"
}

print(client.execute(query, variable_values=params))

query = gql('''
  mutation login($username: String, $email: String, $password: HashedPassword!) {
    loginWithPassword(username: $username, email: $email, password: $password) {
      id
      token
      tokenExpires
      __typename
    }
  }
''')

params = {
  'email': input('User: '),
  'password': {
    'digest': digest_sha256(getpass()),
    'algorithm': 'sha-256'
  }
}

print(client.execute(query, variable_values=params))