"""
Helper functions
"""


def extract_draft_id(original_id: str) -> int:
    return int(original_id.split("-")[1])
