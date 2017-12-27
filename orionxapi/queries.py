def getOrderBook(marketCode="CHACLP"):
    return {
        "query": "query getOrderBook($marketCode: ID!) {\n  orderBook: marketOrderBook(marketCode: $marketCode, limit: 50) {\n    buy {\n      limitPrice\n      amount\n      __typename\n    }\n    sell {\n      limitPrice\n      amount\n      __typename\n    }\n    spread\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode
        },
        "operationName": "getOrderBook"
    }

def getMarketStats(marketCode="CHACLP", aggregation="h1"):
    return {
        "query": "query getMarketStats($marketCode: ID!, $aggregation: MarketStatsAggregation!) {\n  marketStats(marketCode: $marketCode, aggregation: $aggregation) {\n    _id\n    open\n    close\n    high\n    low\n    volume\n    count\n    fromDate\n    toDate\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode,
            "aggregation": aggregation
        },
        "operationName": "getMarketStats"
    }

def getMarketIdleData(code="CHACLP"):
    return {
        "query": "query getMarketIdleData($code: ID) {\n  market(code: $code) {\n    code\n    lastTrade {\n      price\n      __typename\n    }\n    secondaryCurrency {\n      code\n      units\n      format\n      longFormat\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "code": code
        },
        "operationName": "getMarketIdleData"
    }

def getMarket(code="CHACLP"):
    return {
        "query": "query getMarket($code: ID!) {\n  market(code: $code) {\n    code\n    name\n    commission\n    mainCurrency {\n      ...getMarketCurrency\n      __typename\n    }\n    secondaryCurrency {\n      ...getMarketCurrency\n      __typename\n    }\n    __typename\n  }\n  me {\n    _id\n    marketFees(marketCode: $code) {\n      maker\n      taker\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment getMarketCurrency on Currency {\n  code\n  name\n  format\n  longFormat\n  units\n  symbol\n  round\n  wallet {\n    _id\n    balance\n    availableBalance\n    __typename\n  }\n  __typename\n}\n",
        "variables": {
            "code": code
        },
        "operationName": "getMarket"
    }

def myOrders(marketCode="CHACLP"):
    return {
        "query": "query myOrders($marketCode: ID!) {\n  orders(marketCode: $marketCode, onlyOpen: true, limit: 0) {\n    totalCount\n    items {\n      _id\n      sell\n      type\n      amount\n      amountToHold\n      secondaryAmount\n      filled\n      secondaryFilled\n      limitPrice\n      createdAt\n      isStop\n      status\n      stopPriceUp\n      stopPriceDown\n      market {\n        name\n        code\n        mainCurrency {\n          code\n          format\n          longFormat\n          units\n          __typename\n        }\n        secondaryCurrency {\n          code\n          format\n          longFormat\n          units\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode
        },
        "operationName": "myOrders"
    }

def getHistory(marketCode="CHACLP"):
    return {
        "query": "query getHistory($marketCode: ID!) {\n  history: marketTradeHistory(marketCode: $marketCode) {\n    _id\n    amount\n    price\n    date\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode
        },
        "operationName": "getHistory"
    }

def cancelOrder(orderId):
    return {
        "query": "mutation cancelOrder($orderId: ID) {\n  cancelOrder(orderId: $orderId) {\n    _id\n    __typename\n  }\n}\n",
        "variables": {
            "orderId": orderId
        },
        "operationName": "cancelOrder"
    }

def placeLimitOrder(marketCode="CHACLP", amount=20000000, limitPrice=7000, sell=True):
    return {
        "query": "mutation placeLimitOrder($marketCode: ID, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean) {\n  placeLimitOrder(marketCode: $marketCode, amount: $amount, limitPrice: $limitPrice, sell: $sell) {\n    _id\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode,
            "amount": amount,
            "limitPrice": limitPrice,
            "sell": sell
        },
        "operationName": "placeLimitOrder"
    }

def myClosedOrders(marketCode="CHACLP", page=1):
    return {
        "query": "query myClosedOrders($marketCode: ID!, $page: Int) {\n  orders(marketCode: $marketCode, onlyClosed: true, limit: 50, page: $page) {\n    totalCount\n    hasNextPage\n    page\n    items {\n      _id\n      sell\n      type\n      amount\n      amountToHold\n      secondaryAmount\n      filled\n      closedAt\n      secondaryFilled\n      limitPrice\n      createdAt\n      activatedAt\n      isStop\n      status\n      stopPriceUp\n      stopPriceDown\n      market {\n        name\n        code\n        mainCurrency {\n          code\n          format\n          longFormat\n          units\n          __typename\n        }\n        secondaryCurrency {\n          code\n          format\n          longFormat\n          units\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode,
            "page": page
        },
        "operationName": "myClosedOrders"
    }

def placeMarketOrder(marketCode="CHACLP", amount=1000, sell=False):
    return {
        "query": "mutation placeMarketOrder($marketCode: ID, $amount: BigInt, $sell: Boolean) {\n  placeMarketOrder(marketCode: $marketCode, amount: $amount, sell: $sell) {\n    _id\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode,
            "amount": amount,
            "sell": sell
        },
        "operationName": "placeMarketOrder"
    }

def placeStopLimitOrder(marketCode="CHACLP", amount=100000000000000, limitPrice=10000, sell=False, stopPriceUp=40000, stopPriceDown=40000):
    return {
        "query": "mutation placeStopLimitOrder($marketCode: ID, $stopPriceUp: BigInt, $stopPriceDown: BigInt, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean) {\n  placeStopLimitOrder(marketCode: $marketCode, stopPriceUp: $stopPriceUp, stopPriceDown: $stopPriceDown, amount: $amount, limitPrice: $limitPrice, sell: $sell) {\n    _id\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode,
            "amount": amount,
            "limitPrice": limitPrice,
            "sell": sell,
            "stopPriceUp": stopPriceUp,
            "stopPriceDown": stopPriceDown
        },
        "operationName": "placeStopLimitOrder"
    }

def getMyTwoFactorSettings():
    return {
        "query": "query getMyTwoFactorSettings {\n  me {\n    _id\n    profile {\n      firstName\n      lastName\n      __typename\n    }\n    hasTwoFactor\n    __typename\n  }\n}\n",
        "variables": {},
        "operationName": "getMyTwoFactorSettings"
    }

def getMarkets():
    return {
        "query": "query getMarkets {\n  clpMarkets: markets(secondaryCurrencyCode: \"CLP\") {\n    ...exchangeNavbarMarkets\n    __typename\n  }\n  btcMarkets: markets(secondaryCurrencyCode: \"BTC\") {\n    ...exchangeNavbarMarkets\n    __typename\n  }\n}\n\nfragment exchangeNavbarMarkets on Market {\n  code\n  name\n  lastTrade {\n    price\n    __typename\n  }\n  currentStats(aggregation: d1) {\n    close\n    open\n    volume\n    variation\n    __typename\n  }\n  secondaryCurrency {\n    symbol\n    format\n    units\n    __typename\n  }\n  __typename\n}\n",
        "variables": {},
        "operationName": "getMarkets"
    }

def marketCurrentStats(marketCode="CHACLP"):
    return {
        "query": "query marketCurrentStats($marketCode: ID!) {\n  market(code: $marketCode) {\n    code\n    name\n    lastTrade {\n      price\n      __typename\n    }\n    mainCurrency {\n      code\n      units\n      format\n      __typename\n    }\n    secondaryCurrency {\n      code\n      units\n      format\n      __typename\n    }\n    __typename\n  }\n  stats: marketCurrentStats(marketCode: $marketCode, aggregation: d1) {\n    close\n    volume\n    variation\n    __typename\n  }\n}\n",
        "variables": {
            "marketCode": marketCode
        },
        "operationName": "marketCurrentStats"
    }

def getEstimate(marketCode="CHACLP", amount=100000000, sell=False):
    return {
        "query": "query getEstimate($marketCode: ID!, $amount: Float!, $sell: Boolean!) {\n      estimate: marketEstimateAmountToRecieve(marketCode: $marketCode, amount: $amount, sell: $sell)\n    }\n  ",
        "variables": {
            "marketCode": marketCode,
            "amount": amount,
            "sell": sell
        },
        "operationName": "getEstimate"
    }

def getMarketMid(marketCode="CHACLP"):
    return {
        "query": "query getMarketMid($marketCode: ID!) {\n      orderBook: marketOrderBook(marketCode: $marketCode) {\n        mid\n      }\n    }\n  ",
        "variables": {
            "marketCode": marketCode
        },
        "operationName": "getMarketMid"
    }

def getDepthData(marketCode="CHACLP", limit=100):
    return {
        "query": "query getDepthData($marketCode: ID!, $limit: Int) {\n      orderBook: marketOrderBook(marketCode: $marketCode, limit: $limit) {\n        mid\n        buy {\n          limitPrice\n          accumulated\n          accumulatedPrice\n        }\n        sell {\n          limitPrice\n          accumulated\n          accumulatedPrice\n        }\n      }\n    }\n  ",
        "variables": {
            "marketCode": marketCode,
            "limit": limit
        },
        "operationName": "getDepthData"
    }

def createNewAddress(walletId):
    return {
        "query": "mutation createNewAddress($walletId: ID) {\n  createNewAddress(walletId: $walletId) {\n    _id\n    lastCryptoAddress {\n      _id\n      code\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "walletId": walletId
        },
        "operationName": "createNewAddress"
    }

def getWallet(code="BTC"):
    return {
        "query": "query getWallet($code: ID) {\n  me {\n    _id\n    __typename\n  }\n  wallet(code: $code) {\n    _id\n    currency {\n      code\n      units\n      isCrypto\n      format\n      longFormat\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "code": code
        },
        "operationName": "getWallet"
    }

def getCurrencyInfo(code="BTC"):
    return {
        "query": "query getCurrencyInfo($code: ID!) {\n  me {\n    _id\n    __typename\n  }\n  wallet(code: $code) {\n    _id\n    __typename\n  }\n  currency(code: $code) {\n    code\n    units\n    round\n    symbol\n    format\n    isCrypto\n    name\n    __typename\n  }\n  ...noCryptoRecieve\n  ...cryptoRecieve\n}\n\nfragment noCryptoRecieve on Query {\n  me {\n    limits(currencyCode: $code) {\n      totalInInMonth\n      availableInInMonth\n      limit\n      __typename\n    }\n    bankAccounts(currencyCode: $code) {\n      _id\n      name\n      verified\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment cryptoRecieve on Query {\n  me {\n    _id\n    __typename\n  }\n  wallet(code: $code) {\n    _id\n    lastCryptoAddress {\n      _id\n      code\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
        "variables": {
            "code": code
        },
        "operationName": "getCurrencyInfo"
    }

def updateWalletBalance(walletId):
    return {
        "query": "mutation updateWalletBalance($walletId: ID) {\n  updateWalletBalance(walletId: $walletId) {\n    _id\n    balance\n    availableBalance\n    unconfirmedBalance\n    __typename\n  }\n}\n",
        "variables": {
            "walletId": walletId
        },
        "operationName": "updateWalletBalance"
    }

def getLastWalletTransactions(walletId):
    return {
        "query": "query getLastWalletTransactions($walletId: ID) {\n  transactions(walletId: $walletId, limit: 5, sortBy: \"date\", sortType: DESC) {\n    items {\n      _id\n      ...walletLastTransactions\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment walletLastTransactions on Transaction {\n  amount\n  date\n  type\n  adds\n  balance\n  commission\n  description\n  hash\n  explorerURL\n  market {\n    mainCurrency {\n      code\n      __typename\n    }\n    __typename\n  }\n  pairCurrency {\n    name\n    __typename\n  }\n  __typename\n}\n",
        "variables": {
            "walletId": walletId
        },
        "operationName": "getLastWalletTransactions"
    }

def paginated_transactions(walletId, limit=10, page=1, sortBy="date", sortType="DESC"):
    return {
        "query": "query paginated_transactions($page: Int, $limit: Int, $sortBy: String, $sortType: SortType, $filter: String, $walletId: ID) {\n  result: transactions(page: $page, limit: $limit, sortBy: $sortBy, sortType: $sortType, filter: $filter, walletId: $walletId) {\n    _id\n    totalCount\n    totalPages\n    hasNextPage\n    hasPreviousPage\n    items {\n      _id\n      adds\n      amount\n      commission\n      balance\n      type\n      date\n      market {\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "limit": limit,
            "page": page,
            "sortBy": sortBy,
            "sortType": sortType,
            "walletId": walletId
        },
        "operationName": "paginated_transactions"
    }

def getMyPaymentsWithError():
    return {
        "query": "query getMyPaymentsWithError {\n  currency(code: \"CLP\") {\n    code\n    format\n    symbol\n    units\n    __typename\n  }\n  me {\n    _id\n    paymentsWithError {\n      _id\n      createdAt\n      origin\n      originName\n      originRut\n      originBank\n      amount\n      error\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {},
        "operationName": "getMyPaymentsWithError"
    }

def getMyVerification():
    return {
        "query": "query getMyVerification {\n  me {\n    _id\n    verification {\n      verifiedLevel {\n        code\n        name\n        __typename\n      }\n      nextLevel {\n        code\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {},
        "operationName": "getMyVerification"
    }

def getUserWallets():
    return {
        "query": "query getUserWallets {\n  me {\n    _id\n    wallets {\n      currency {\n        code\n        __typename\n      }\n      ...walletListItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment walletListItem on Wallet {\n  _id\n  balance\n  currency {\n    code\n    units\n    name\n    symbol\n    format\n    isCrypto\n    minimumAmountToSend\n    __typename\n  }\n  __typename\n}\n",
        "variables": {},
        "operationName": "getUserWallets"
    }

def addressIsInternal(address="", currencyCode="BTC"):
    return {
        "query": "query ($address: ID, $currencyCode: ID!) {\n  isInternal: addressIsInternal(address: $address, currencyCode: $currencyCode)\n}\n",
        "variables": {
            "address": address,
            "currencyCode": currencyCode
        },
        "operationName": None
    }


def send(fromWalletId, toAddressCode, amount=100000000, fee=110):
    return {
        "query": "mutation send($fromWalletId: ID!, $toAddressCode: ID!, $amount: BigInt!, $fee: BigInt!, $description: String, $twoFactorCode: String) {\n  sendCrypto(fromWalletId: $fromWalletId, toAddressCode: $toAddressCode, amount: $amount, fee: $fee, description: $description, twoFactorCode: $twoFactorCode) {\n    _id\n    __typename\n  }\n}\n",
        "variables": {
            "fromWalletId": fromWalletId,
            "toAddressCode": toAddressCode,
            "amount": amount,
            "fee": fee
        },
        "operationName": "send"
    }

def currencyTransformFactor(inCurrencyCode="BTC", outCurrencyCode=None):
    return {
        "query": "query currencyTransformFactor($inCurrencyCode: ID!, $outCurrencyCode: ID) {\n  currencyTransformFactor(inCurrencyCode: $inCurrencyCode, outCurrencyCode: $outCurrencyCode) {\n    factor\n    outCurrency {\n      code\n      units\n      format\n      symbol\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "inCurrencyCode": inCurrencyCode,
            "outCurrencyCode": outCurrencyCode
        },
        "operationName": "currencyTransformFactor"
    }

def getMe():
    return {
        "query": "query getMe {\n  me {\n    _id\n    intercomHash\n    email\n    createdAt\n    roles\n    profile {\n      firstName\n      lastName\n      phone\n      phoneVerified\n      __typename\n    }\n      emails {\n      address\n      verified\n      __typename\n    }\n    __typename\n  }\n}\n",
        "operationName": "getMe"
    }

def paginated_cryptoAddresses(userId, limit=10, page=1, currencyCode="CHA"):
    return {
        "query": "query paginated_cryptoAddresses($page: Int, $limit: Int, $sortBy: String, $sortType: SortType, $filter: String, $currencyCode: ID!, $userId: ID) {\n  result: cryptoAddresses(page: $page, limit: $limit, sortBy: $sortBy, sortType: $sortType, filter: $filter, currencyCode: $currencyCode, userId: $userId) {\n    _id\n    totalCount\n    totalPages\n    hasNextPage\n    hasPreviousPage\n    items {\n      _id\n      code\n      updatedAt\n      createdAt\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "limit": limit,
            "page": page,
            "currencyCode": currencyCode,
            "userId": userId
        },
        "operationName": "paginated_cryptoAddresses"
    }
#[{"data":{"placeLimitOrder":null},"errors":[{"message":"Fondos insuficientes, tienes 0 [insufficientFunds]","path":["placeLimitOrder"],"details":{"code":"insufficientFunds","reason":"Fondos insuficientes, tienes 0","errorType":"userError"}}]}]