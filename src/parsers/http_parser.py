from typing import List, Dict
from src.models.event import Event


def parse_http_log(filepath: str) -> List[Event]:
    events: List[Event] = []
    field_index: Dict[str, int] = {}

    with open(filepath, "r") as f:
        for line in f:
            # Capture field indices from Zeek header
            if line.startswith("#fields"):
                headers = line.strip().split("\t")[1:]
                field_index = {name: i for i, name in enumerate(headers)}
                continue

            # Skip other metadata
            if line.startswith("#"):
                continue

            fields = line.strip().split("\t")

            try:
                ts = float(fields[field_index["ts"]])
                src_ip = fields[field_index["id.orig_h"]]
                dst_ip = fields[field_index["id.resp_h"]]
                method = fields[field_index["method"]]
                host = fields[field_index["host"]]
                uri = fields[field_index["uri"]]

                req_len = fields[field_index["request_body_len"]]
                resp_len = fields[field_index["response_body_len"]]
                status_code = fields[field_index["status_code"]]

                try:
                    success = int(status_code) < 400
                except ValueError:
                    success = None

                try:
                    total_bytes = int(req_len) + int(resp_len)
                except ValueError:
                    total_bytes = None

                resource = f"{host}{uri}"

                event = Event(
                    timestamp=ts,
                    source_ip=src_ip,
                    dest_ip=dst_ip,
                    protocol="tcp",
                    service="http",
                    action=method,
                    resource=resource,
                    success=success,
                    bytes=total_bytes,
                )

                events.append(event)

            except KeyError:
                # Required field missing
                continue

    return events