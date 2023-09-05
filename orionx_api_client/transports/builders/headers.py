import hmac
import json
import time
from hashlib import sha512
from typing import Any, Dict, List, Union


def hmac_sha512(secret_key: str, timestamp: int, body: str) -> str:
    """
    Generates a HMAC-SHA512 signature.

    Args:
        secret_key: The secret key to use for HMAC signing.
        timestamp: The timestamp to be included in the message.
        body: The request body.

    Returns:
        str: The HMAC-SHA512 signature.
    """
    key = bytearray(secret_key, "utf-8")
    msg = str(timestamp) + str(body)
    msg = msg.encode("utf-8")
    return hmac.HMAC(key, msg, sha512).hexdigest()


def get_unix_timestamp_in_ms() -> int:
    """
    Retrieves the current time in UNIX format (milliseconds since the epoch).

    Returns: The current time in milliseconds.
    """
    return int(time.time() * 1000)


class HeadersBuilder:
    """
    Construct request headers required for OrionX API authentication.

    Attributes:
        api_key: The user-specific API key.
        secret_key: The user-specific secret key.
    """
    def __init__(self, api_key: str, secret_key: str) -> None:
        """
        Initialize the header builder with API credentials.

        Args:
            api_key: The user's API key.
            secret_key: The user's secret key for signing.
        """
        self.api_key = api_key
        self.secret_key = secret_key

    def build(
        self,
        payload: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> Dict[str, str]:
        """
        Build request headers for OrionX API requests.

        The headers include Content-Type, timestamp, \
            API key, and a HMAC-SHA512 signature.

        Args:
            payload: Request payload to be sent. 

        Returns: Formulated request headers for OrionX API.
        """
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
