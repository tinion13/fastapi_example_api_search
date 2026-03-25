from datetime import UTC, datetime, timedelta, timezone


def format_ts_to_str(ts: int, tz_shift: int) -> str:
    tz = timezone(timedelta(seconds=tz_shift))
    return datetime.fromtimestamp(ts, tz=UTC).astimezone(tz).strftime("%Y.%m.%d %H:%M")
