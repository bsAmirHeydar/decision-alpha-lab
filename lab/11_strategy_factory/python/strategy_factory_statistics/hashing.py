def fnv1a64_utf16le(text: str) -> int:
    h = 0xCBF29CE484222325
    for b in text.encode("utf-16le"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h

def stable_id(prefix: str, payload: str) -> str:
    return f"{prefix}_{fnv1a64_utf16le(payload):016x}"
