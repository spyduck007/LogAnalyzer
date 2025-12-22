# Unified Event Schema

To enable consistent detection logic across different log formats, this project
maps all log entries into a unified event abstraction.

This schema represents a single observable action initiated by a source entity.

---

## Event Fields

Event:
- timestamp
- source_ip
- dest_ip
- protocol
- service
- action
- resource
- success
- bytes

---

## HTTP Log Mapping

### Source
Zeek: http.log

### Field Mapping

- Event.timestamp  ← ts
- Event.source_ip  ← id.orig_h
- Event.dest_ip    ← id.resp_h
- Event.protocol   ← "tcp"
- Event.service    ← "http"
- Event.action     ← "request"
- Event.resource   ← host + uri
- Event.success    ← (status_code < 400)
- Event.bytes      ← request_body_len + response_body_len

### Notes

- POST requests are emphasized for brute force detection
- Repeated failures to the same resource indicate authentication attempts
- High URI diversity from a single source indicates scanning behavior

---

## SSH Log Mapping (Inferred)

### Source
Zeek: conn.log

### Field Mapping

- Event.timestamp  ← ts
- Event.source_ip  ← id.orig_h
- Event.dest_ip    ← id.resp_h
- Event.protocol   ← proto
- Event.service    ← "ssh" (if id.resp_p == 22)
- Event.action     ← "connect"
- Event.resource   ← "ssh"
- Event.success    ← inferred
- Event.bytes      ← orig_bytes + resp_bytes

### SSH Success Inference

Authentication success or failure is inferred using:
- Connection duration
- Total bytes transferred
- Repeated short-lived sessions from the same source

Short-lived connections with minimal data transfer are treated as failed
authentication attempts.

---

## Aggregation Model

Events are aggregated over fixed time windows per source IP.

Detection logic operates on these aggregated windows, not on individual events.

---

## Limitations

- Authentication success is inferred, not explicit
- Encrypted payloads are not inspected
- Thresholds may require tuning per dataset

These limitations are acknowledged and documented.
