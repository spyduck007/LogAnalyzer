from collections import defaultdict
from typing import List, Dict
from src.models.event import Event


def group_events_by_window(
    events: List[Event],
    window_size: int
) -> Dict[str, List[Event]]:
    """
    Group events by (source_ip, time window).
    Window size is in seconds.
    """

    windows: Dict[str, List[Event]] = defaultdict(list)

    for event in events:
        window_id = int(event.timestamp // window_size)
        key = f"{event.source_ip}:{window_id}"
        windows[key].append(event)

    return windows
