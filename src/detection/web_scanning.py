from typing import List
from src.models.event import Event


def detect_web_scanning(
    events: List[Event],
    min_requests: int = 30,
    min_unique_resources: int = 20
) -> bool:
    http_events = [
        e for e in events
        if e.service == "http"
    ]

    if len(http_events) < min_requests:
        return False

    resources = set(e.resource for e in http_events if e.resource)

    return len(resources) >= min_unique_resources
