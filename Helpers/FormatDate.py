from datetime import datetime, timezone

def format_datetime(dt: datetime) -> str:
    # ISO 8601 UTC formatında, milisaniyesiz string döndürür
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")