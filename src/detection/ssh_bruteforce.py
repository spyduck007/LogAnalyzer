from typing import List
from src.models.event import Event


def detect_ssh_bruteforce(
    events: List[Event],
    min_attempts: int = 10,
    max_success_ratio: float = 0.2
) -> bool:
    ssh_events = [
        e for e in events
        if e.service == "ssh"
    ]

    if len(ssh_events) < min_attempts:
        return False

    successes = sum(1 for e in ssh_events if e.success is True)
    total = len(ssh_events)

    return (successes / total) <= max_success_ratio
