from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    timestamp: float
    source_ip: str
    dest_ip: str
    protocol: str
    service: str
    action: str
    resource: Optional[str]
    success: Optional[bool]
    bytes: Optional[int]
