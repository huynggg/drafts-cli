from datetime import datetime
import pytz
"""
Helper functions
"""


# TODO: This should accept timezone as params
def format_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    central = pytz.timezone("America/Chicago")
    central_dt = dt.astimezone(central)
    # Format it to mm/dd/yyyy hh:mm, for showing to user
    return central_dt.strftime("%m/%d/%Y %H:%M")
