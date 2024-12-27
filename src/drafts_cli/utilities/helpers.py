from datetime import datetime
"""
Helper functions
"""


def format_timestamp(timestamp: str) -> str:
    # Parse the input timestamp
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    # Format it to mm/dd/yyyy hh:mm
    return dt.strftime("%m/%d/%Y %H:%M")
