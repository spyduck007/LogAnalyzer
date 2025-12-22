# Log Selection

This project analyzes a small, intentionally chosen subset of logs derived
from network traffic using the Zeek network analysis framework.

The goal is to detect specific attacker behaviors using interpretable signals,
not to exhaustively analyze all available telemetry.

---

## Logs Used

### 1. http.log

**Purpose:** Detect web brute force and web scanning behavior.

**Rationale:**

- Captures individual HTTP requests
- Exposes request method, URI, and response status
- Enables modeling of request frequency, failure rate, and resource diversity

This log provides the primary signal for detecting:

- Repeated login attempts
- Automated scanning activity

---

### 2. conn.log

**Purpose:** Infer SSH brute force behavior and session-level patterns.

**Rationale:**

- Records all TCP connection metadata
- Allows identification of connections to port 22 (SSH)
- Enables inference of failed authentication based on short-lived sessions
  and low byte counts

This log provides indirect but sufficient information to model SSH brute force
behavior without inspecting payloads.

---

### 3. dns.log (Optional)

**Purpose:** Supplement web scanning detection.

**Rationale:**

- Reveals domain enumeration and discovery behavior
- Provides context for web access patterns

This log is not required for core detection and may be excluded in early stages.

---

## Logs Explicitly Excluded

The following logs are not used in the current scope:

- ssh.log (authentication-level details)
- ssl.log, x509.log (encrypted session metadata)
- weird.log (high-noise anomaly reports)
- file and protocol-specific logs (FTP, SMB, LDAP, etc.)

These logs are excluded to maintain focus and reduce false positives.

---

## Summary

This project prioritizes:

- Behavioral signals over protocol completeness
- Interpretable metadata over payload inspection
- Focused scope over broad telemetry
