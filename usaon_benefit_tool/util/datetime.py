from datetime import datetime
from zoneinfo import ZoneInfo


def today_mountain():
    """Get today's date in Mountain Time."""
    return datetime.now(ZoneInfo("America/Denver")).date()
