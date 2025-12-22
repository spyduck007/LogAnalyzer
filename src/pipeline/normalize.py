from typing import List
from src.models.event import Event
from src.parsers.http_parser import parse_http_log
from src.parsers.conn_parser import parse_conn_log


def load_events(
    http_log_path: str,
    ssh_log_path: str
) -> List[Event]:
    """
    Load and normalize HTTP and SSH events into a single
    time-ordered event stream.
    """

    http_events = parse_http_log(http_log_path)
    ssh_events = parse_conn_log(ssh_log_path)

    all_events = http_events + ssh_events

    # Sort globally by timestamp
    all_events.sort(key=lambda e: e.timestamp)

    return all_events
