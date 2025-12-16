import hmac
import hashlib
from typing import Tuple


def compute_hmac_sha256_hex(secret: str, body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def verify_signature(*, secret: str, body: bytes, signature_header: str) -> Tuple[bool, str]:
    """
    Returns: (is_valid, expected_signature_hex)
    """
    expected = compute_hmac_sha256_hex(secret, body)
    provided = (signature_header or "").strip()

    # constant-time compare
    is_valid = hmac.compare_digest(provided, expected)
    return is_valid, expected
