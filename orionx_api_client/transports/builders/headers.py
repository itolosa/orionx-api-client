import hmac
import json
import time
from hashlib import sha512
from typing import Any, Dict, List, Union


def hmac_sha512(secret_key: str, timestamp: int, body: str) -> str:
    key = bytearray(secret_key, "utf-8")
    msg = str(timestamp) + str(body)
    msg = msg.encode("utf-8")
    return hmac.HMAC(key, msg, sha512).hexdigest()


def get_unix_timestamp_in_ms() -> int:
    return int(time.time() * 1000)


class HeadersBuilder:
    def __init__(self, api_key: str, secret_key: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key

    def build(
        self,
        payload: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> Dict[str, str]:
        data = json.dumps(payload)
        timestamp = get_unix_timestamp_in_ms()
        signature = hmac_sha512(self.secret_key, timestamp, data)

        headers = {
            "Content-Type": "application/json",
            "X-ORIONX-TIMESTAMP": f"{timestamp}",
            "X-ORIONX-APIKEY": self.api_key,
            "X-ORIONX-SIGNATURE": signature,
        }

        return headers
