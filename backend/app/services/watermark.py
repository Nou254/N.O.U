"""
Invisible question watermarks.

Each question drawn into an assessment session gets a unique invisible
watermark token embedded in its text. The token ("NOUWM:<hex>") is encoded
entirely in zero-width Unicode characters (U+200B, U+200C, U+200D, U+FEFF),
so it renders as nothing on screen but still rides along when the question
text is copied into an AI tool. The grading prompt tells Groq to look for
these tokens (plus general AI-writing signals) so the admin can see which
answers were likely produced with AI assistance.
"""

import re
import secrets

# Zero-width alphabet: 4 symbols -> 2 bits each. None of these render.
_ZERO_WIDTH = ["\u200b", "\u200c", "\u200d", "\ufeff"]
_ZW_RUN_RE = re.compile(f"[{re.escape(''.join(_ZERO_WIDTH))}]+")

# Old (visible) frame format used before zero-width encoding:
# \u200bNOUWM:<hex>\u200b - kept so legacy rows can be stripped/migrated.
_OLD_FRAME_RE = re.compile("\u200bNOUWM:([0-9a-f]+)\u200b")

_PAYLOAD_PREFIX = "NOUWM:"


def generate_watermark(length: int = 8) -> str:
    """Return a random hex watermark token (default 8 characters)."""
    return secrets.token_hex((length + 1) // 2)[:length]


def _encode(payload: str) -> str:
    """Encode an ASCII payload into zero-width characters (2 bits per char)."""
    out = []
    for byte in payload.encode("ascii"):
        out.append(_ZERO_WIDTH[(byte >> 6) & 0b11])
        out.append(_ZERO_WIDTH[(byte >> 4) & 0b11])
        out.append(_ZERO_WIDTH[(byte >> 2) & 0b11])
        out.append(_ZERO_WIDTH[byte & 0b11])
    return "".join(out)


def _decode(encoded: str) -> str:
    """Decode a zero-width-encoded string back to its ASCII payload."""
    lut = {ch: i for i, ch in enumerate(_ZERO_WIDTH)}
    out = bytearray()
    current = 0
    bits = 0
    for ch in encoded:
        if ch not in lut:
            continue
        current = (current << 2) | lut[ch]
        bits += 2
        if bits == 8:
            out.append(current)
            current = 0
            bits = 0
    try:
        return out.decode("ascii")
    except UnicodeDecodeError:
        return ""


def embed_watermark(text: str, token: str) -> str:
    """Append an invisible (zero-width encoded) watermark frame to the text."""
    return f"{text}{_encode(_PAYLOAD_PREFIX + token)}"


def extract_watermarks(text: str) -> list:
    """Return all watermark payloads (e.g. 'NOUWM:1a2b3c4d') in the given text."""
    found = []
    for match in _ZW_RUN_RE.findall(text or ""):
        payload = _decode(match)
        if payload.startswith(_PAYLOAD_PREFIX):
            found.append(payload)
    # Legacy rows embedded with the old visible format.
    for token in _OLD_FRAME_RE.findall(text or ""):
        found.append(_PAYLOAD_PREFIX + token)
    return found


def strip_watermarks(text: str) -> str:
    """Remove watermark frames from text (zero-width + legacy visible formats)."""
    if not text:
        return text
    cleaned = _OLD_FRAME_RE.sub("", text)
    return _ZW_RUN_RE.sub("", cleaned)


def has_watermark(text: str, token: str) -> bool:
    """True when the text carries the given watermark token."""
    return _PAYLOAD_PREFIX + token in extract_watermarks(text or "")
