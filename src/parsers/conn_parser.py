from typing import List, Dict
from src.models.event import Event


def parse_conn_log(filepath: str) -> List[Event]:
    events: List[Event] = []
    field_index: Dict[str, int] = {}

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#fields"):
                headers = line.strip().split("\t")[1:]
                field_index = {name: i for i, name in enumerate(headers)}
                continue

            if line.startswith("#"):
                continue

            fields = line.strip().split("\t")

            try:
                if fields[field_index["id.resp_p"]] != "22":
                    continue

                ts = float(fields[field_index["ts"]])
                src_ip = fields[field_index["id.orig_h"]]
                dst_ip = fields[field_index["id.resp_h"]]
                proto = fields[field_index["proto"]]

                duration = fields[field_index["duration"]]
                orig_bytes = fields[field_index["orig_bytes"]]
                resp_bytes = fields[field_index["resp_bytes"]]

                try:
                    duration_val = float(duration)
                    byte_count = int(orig_bytes) + int(resp_bytes)
                    success = duration_val > 1.0 and byte_count > 1000
                except ValueError:
                    success = None

                event = Event(
                    timestamp=ts,
                    source_ip=src_ip,
                    dest_ip=dst_ip,
                    protocol=proto,
                    service="ssh",
                    action="connect",
                    resource="ssh",
                    success=success,
                    bytes=None,
                )

                events.append(event)

            except KeyError:
                continue

    return events
