from typing import List
from src.models.event import Event


def detect_web_bruteforce(
    events: List[Event],
    min_requests: int = 20,
    max_unique_resources: int = 2
) -> bool:
    """
    Detect web brute force attempts based on repeated access
    to a small set of resources.
    """

    http_events = [
        e for e in events
        if e.service == "http"
    ]

    if len(http_events) < min_requests:
        return False

    resources = set(e.resource for e in http_events if e.resource)

    # Many requests, few targets → brute force
    return len(resources) <= max_unique_resources
