
# marketOrderBook
query = gql('''
  query getOrderBook($marketCode: ID!) {
    orderBook: marketOrderBook(marketCode: $marketCode, limit: 50) {
      buy {
        limitPrice
        amount
        __typename
      }
      sell {
        limitPrice
        amount
        __typename
      }
      spread
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP"
}

operation_name = "getOrderBook"

# marketStats
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

operation_name = "getMarketStats"

# market
query = gql('''
  query getMarketIdleData($code: ID) {
    market(code: $code) {
      code
      lastTrade {
        price
        __typename
      }
      secondaryCurrency {
        code
        units
        format
        longFormat
        __typename
      }
      __typename
    }
  }
''')

params = {
  "code": "CHACLP"
}

operation_name = "getMarketIdleData"

# market
query = gql('''
  query getMarket($code: ID!) {
    market(code: $code) {
      code
      name
      commission
      mainCurrency {
        ...getMarketCurrency
        __typename
      }
      secondaryCurrency {
        ...getMarketCurrency
        __typename
      }
      __typename
    }
    me {
      _id
      marketFees(marketCode: $code) {
        maker
        taker
        __typename
      }
      __typename
    }
  }

  fragment getMarketCurrency on Currency {
    code
    name
    format
    longFormat
    units
    symbol
    round
    wallet {
      _id
      balance
      availableBalance
      __typename
    }
    __typename
  }
''')

params = {
  "code": "CHACLP"
}

operation_name = "getMarket"

# orders
query = gql('''
  query myOrders($marketCode: ID!) {
    orders(marketCode: $marketCode, onlyOpen: true, limit: 0) {
      totalCount
      items {
        _id
        sell
        type
        amount
        amountToHold
        secondaryAmount
        filled
        secondaryFilled
        limitPrice
        createdAt
        isStop
        status
        stopPriceUp
        stopPriceDown
        market {
          name
          code
          mainCurrency {
            code
            format
            longFormat
            units
            __typename
          }
          secondaryCurrency {
            code
            format
            longFormat
            units
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP"
}

operation_name = "myOrders"


# marketTradeHistory
query = gql('''
  query getHistory($marketCode: ID!) {
    history: marketTradeHistory(marketCode: $marketCode) {
      _id
      amount
      price
      date
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP"
}

operation_name = "getHistory"


# cancelOrder
query = gql('''
  mutation cancelOrder($orderId: ID) {
    cancelOrder(orderId: $orderId) {
      _id
      __typename
    }
  }
''')

params = {
  "orderId": ''
}

operation_name = "cancelOrder"


# placeLimitOrder
query = gql('''
  mutation placeLimitOrder($marketCode: ID, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean) {
    placeLimitOrder(marketCode: $marketCode, amount: $amount, limitPrice: $limitPrice, sell: $sell) {
      _id
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "amount": 2,
  "limitPrice": 3,
  "sell": True
}

operation_name = "placeLimitOrder"

# orders
query = gql('''
  query myClosedOrders($marketCode: ID!, $page: Int) {
    orders(marketCode: $marketCode, onlyClosed: true, limit: 50, page: $page) {
      totalCount
      hasNextPage
      page
      items {
        _id
        sell
        type
        amount
        amountToHold
        secondaryAmount
        filled
        closedAt
        secondaryFilled
        limitPrice
        createdAt
        activatedAt
        isStop
        status
        stopPriceUp
        stopPriceDown
        market {
          name
          code
          mainCurrency {
            code
            format
            longFormat
            units
            __typename
          }
          secondaryCurrency {
            code
            format
            longFormat
            units
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "page": 1
}

operation_name = "myClosedOrders"

# placeMarketOrder
query = gql('''
  mutation placeMarketOrder($marketCode: ID, $amount: BigInt, $sell: Boolean) {
    placeMarketOrder(marketCode: $marketCode, amount: $amount, sell: $sell) {
      _id
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "amount": 1,
  "sell": True
}

operation_name = "placeMarketOrder"

# placeStopLimitOrder
query = gql('''
  mutation placeStopLimitOrder($marketCode: ID, $stopPriceUp: BigInt, $stopPriceDown: BigInt, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean) {
    placeStopLimitOrder(marketCode: $marketCode, stopPriceUp: $stopPriceUp, stopPriceDown: $stopPriceDown, amount: $amount, limitPrice: $limitPrice, sell: $sell) {
      _id
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "amount": 1,
  "limitPrice": 2,
  "sell": False,
  "stopPriceUp": 3,
  "stopPriceDown": 4
}

operation_name = "placeStopLimitOrder"


# me
query = gql('''
  query getMyTwoFactorSettings {
    me {
      _id
      profile {
        firstName
        lastName
        __typename
      }
      hasTwoFactor
      __typename
    }
  }
''')

params = {}

operation_name = "getMyTwoFactorSettings"

# markets
query = gql('''
  query getMarkets {
    clpMarkets: markets(secondaryCurrencyCode: \"CLP\") {
      ...exchangeNavbarMarkets
      __typename
    }
    btcMarkets: markets(secondaryCurrencyCode: \"BTC\") {
      ...exchangeNavbarMarkets
      __typename
    }
  }

  fragment exchangeNavbarMarkets on Market {
    code
    name
    lastTrade {
      price
      __typename
    }
    currentStats(aggregation: d1) {
      close
      open
      volume
      variation
      __typename
    }
    secondaryCurrency {
      symbol
      format
      units
      __typename
    }
    __typename
  }
''')

params = {},

operation_name = "getMarkets"


# market
query = gql('''
  query marketCurrentStats($marketCode: ID!) {
    market(code: $marketCode) {
      code
      name
      lastTrade {
        price
        __typename
      }
      mainCurrency {
        code
        units
        format
        __typename
      }
      secondaryCurrency {
        code
        units
        format
        __typename
      }
      __typename
    }
    stats: marketCurrentStats(marketCode: $marketCode, aggregation: d1) {
      close
      volume
      variation
      __typename
    }
  }
'''),
params = {
  "marketCode": "CHACLP"
}

operation_name = "marketCurrentStats"


# marketEstimateAmountToRecieve
query = gql('''
  query getEstimate($marketCode: ID!, $amount: Float!, $sell: Boolean!) {
    estimate: marketEstimateAmountToRecieve(marketCode: $marketCode, amount: $amount, sell: $sell)
  }
''')

params = {
  "marketCode": "CHACLP",
  "amount": 1,
  "sell": False
}

operation_name = "getEstimate"

# marketOrderBook
query = gql('''
  query getMarketMid($marketCode: ID!) {
    orderBook: marketOrderBook(marketCode: $marketCode) {
      mid
    }
  }
''')

params = {
  "marketCode": "CHACLP"
}

operation_name = "getMarketMid"


# marketOrderBook
query = gql('''
  query getDepthData($marketCode: ID!, $limit: Int) {
    orderBook: marketOrderBook(marketCode: $marketCode, limit: $limit) {
      mid
      buy {
        limitPrice
        accumulated
        accumulatedPrice
      }
      sell {
        limitPrice
        accumulated
        accumulatedPrice
      }
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "limit": 100
}

operation_name = "getDepthData"


# createNewAddress
query = gql('''
  mutation createNewAddress($walletId: ID) {
    createNewAddress(walletId: $walletId) {
      _id
      lastCryptoAddress {
        _id
        code
        __typename
      }
      __typename
    }
  }
''')

params = {
  "walletId": "123123"
}

operation_name = "createNewAddress"

# me
# wallet
query = gql('''
  query getWallet($code: ID) {
    me {
      _id
      __typename
    }
    wallet(code: $code) {
      _id
      currency {
        code
        units
        isCrypto
        format
        longFormat
        __typename
      }
      __typename
    }
  }
''')

params = {
  "code": "BTC"
}

operation_name = "getWallet"

# me
# wallet
# currency
query = gql('''
  query getCurrencyInfo($code: ID!) {
    me {
      _id
      __typename
    }
    wallet(code: $code) {
      _id
      __typename
    }
    currency(code: $code) {
      code
      units
      round
      symbol
      format
      isCrypto
      name
      __typename
    }
    ...noCryptoRecieve
    ...cryptoRecieve
  }

  fragment noCryptoRecieve on Query {
    me {
      limits(currencyCode: $code) {
        totalInInMonth
        availableInInMonth
        limit
        __typename
      }
      bankAccounts(currencyCode: $code) {
        _id
        name
        verified
        __typename
      }
      __typename
    }
    __typename
  }

  fragment cryptoRecieve on Query {
    me {
      _id
      __typename
    }
    wallet(code: $code) {
      _id
      lastCryptoAddress {
        _id
        code
        __typename
      }
      __typename
    }
    __typename
  }
''')

params = {
  "code": "BTC"
}

operation_name = "getCurrencyInfo"


# updateWalletBalance
query = gql('''
  mutation updateWalletBalance($walletId: ID) {
    updateWalletBalance(walletId: $walletId) {
      _id
      balance
      availableBalance
      unconfirmedBalance
      __typename
    }
  }
''')

params = {
    "walletId": "123123123"
}

operation_name = "updateWalletBalance"


# transactions
query = gql('''
  query getLastWalletTransactions($walletId: ID) {
    transactions(walletId: $walletId, limit: 5, sortBy: \"date\", sortType: DESC) {
      items {
        _id
        ...walletLastTransactions
        __typename
      }
      __typename
    }
  }

  fragment walletLastTransactions on Transaction {
    amount
    date
    type
    adds
    balance
    commission
    description
    hash
    explorerURL
    market {
      mainCurrency {
        code
        __typename
      }
      __typename
    }
    pairCurrency {
      name
      __typename
    }
    __typename
  }
''')

params = {
  "walletId": "123123"
}

operation_name = "getLastWalletTransactions"


# transactions
query = gql('''
  query paginated_transactions($page: Int, $limit: Int, $sortBy: String, $sortType: SortType, $filter: String, $walletId: ID) {
    result: transactions(page: $page, limit: $limit, sortBy: $sortBy, sortType: $sortType, filter: $filter, walletId: $walletId) {
      _id
      totalCount
      totalPages
      hasNextPage
      hasPreviousPage
      items {
        _id
        adds
        amount
        commission
        balance
        type
        date
        market {
          name
          __typename
        }
        __typename
      }
      __typename
    }
  }
''')

params = {
  "limit": 10,
  "page": 1,
  "sortBy": "date",
  "sortType": "DESC",
  "walletId": "123123"
}

operation_name = "paginated_transactions"


# currency
query = gql('''
  query getMyPaymentsWithError {
    currency(code: \"CLP\") {
      code
      format
      symbol
      units
      __typename
    }
    me {
      _id
      paymentsWithError {
        _id
        createdAt
        origin
        originName
        originRut
        originBank
        amount
        error
        __typename
      }
      __typename
    }
  }
''')

params = {}

operation_name = "getMyPaymentsWithError"



# me
query = gql('''
  query getMyVerification {
    me {
      _id
      verification {
        verifiedLevel {
          code
          name
          __typename
        }
        nextLevel {
          code
          __typename
        }
        __typename
      }
      __typename
    }
  }
''')

params = {}
operation_name = "getMyVerification"

# me
query = gql('''
  query getUserWallets {
    me {
      _id
      wallets {
        currency {
          code
          __typename
        }
        ...walletListItem
        __typename
      }
      __typename
    }
  }

  fragment walletListItem on Wallet {
    _id
    balance
    currency {
      code
      units
      name
      symbol
      format
      isCrypto
      minimumAmountToSend
      __typename
    }
    __typename
  }
''')

params = {}

operation_name = "getUserWallets"


# addressIsInternal
query = gql('''
  query ($address: ID, $currencyCode: ID!) {
    isInternal: addressIsInternal(address: $address, currencyCode: $currencyCode)
  }
''')

params = {
  "address": "",
  "currencyCode": "BTC"
}

operation_name = None



# sendCrypto
query = gql('''
  mutation send($fromWalletId: ID!, $toAddressCode: ID!, $amount: BigInt!, $fee: BigInt!, $description: String, $twoFactorCode: String) {
    sendCrypto(fromWalletId: $fromWalletId, toAddressCode: $toAddressCode, amount: $amount, fee: $fee, description: $description, twoFactorCode: $twoFactorCode) {
      _id
      __typename
    }
  }
''')

params = {
  "fromWalletId": "123123",
  "toAddressCode": "123123",
  "amount": 1,
  "fee": 2
}

operation_name = "send"


# currencyTransformFactor
query = gql('''
  query currencyTransformFactor($inCurrencyCode: ID!, $outCurrencyCode: ID) {
    currencyTransformFactor(inCurrencyCode: $inCurrencyCode, outCurrencyCode: $outCurrencyCode) {
      factor
      outCurrency {
        code
        units
        format
        symbol
        __typename
      }
      __typename
    }
  }
''')

params = {
  "inCurrencyCode": "BTC",
  "outCurrencyCode": None
}

operation_name = "currencyTransformFactor"


# me
query = gql('''
  query getMe {
    me {
      _id
      intercomHash
      email
      createdAt
      roles
      profile {
        firstName
        lastName
        phone
        phoneVerified
        __typename
      }
        emails {
        address
        verified
        __typename
      }
      __typename
    }
  }
''')

operation_name = "getMe"


# cryptoAddresses
query = gql('''
  query paginated_cryptoAddresses($page: Int, $limit: Int, $sortBy: String, $sortType: SortType, $filter: String, $currencyCode: ID!, $userId: ID) {
    result: cryptoAddresses(page: $page, limit: $limit, sortBy: $sortBy, sortType: $sortType, filter: $filter, currencyCode: $currencyCode, userId: $userId) {
      _id
      totalCount
      totalPages
      hasNextPage
      hasPreviousPage
      items {
        _id
        code
        updatedAt
        createdAt
        __typename
      }
      __typename
    }
  }
''')

params = {
  "limit": 10,
  "page": 1,
  "currencyCode": "CHA",
  "userId": "123123"
}

operation_name = "paginated_cryptoAddresses"

#[{"data":{"placeLimitOrder":null},"errors":[{"message":"Fondos insuficientes, tienes 0 [insufficientFunds]","path":["placeLimitOrder"],"details":{"code":"insufficientFunds","reason":"Fondos insuficientes, tienes 0","errorType":"userError"}}]}]