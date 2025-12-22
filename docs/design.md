# Design Document: Explainable Log-Based Intrusion Detection

## 1. Problem Statement

Modern systems generate large volumes of logs that contain weak but meaningful signals of malicious activity.  
The goal of this project is to design and implement a lightweight, explainable intrusion detection framework that identifies suspicious **web and SSH access behavior** from system logs.

Rather than relying on black-box machine learning, this project focuses on **interpretable detection rules and simple statistical models** that make detection decisions understandable and auditable.

---

## 2. Log Sources

This system analyzes the following log types:

### Web Access Logs
- HTTP request logs (method, URI, status code)
- Connection metadata (source IP, destination IP, bytes transferred)

### SSH Connection Logs
- Connection-level metadata for SSH sessions
- Inferred authentication behavior from connection patterns

All logs are **derived from publicly available PCAP datasets** using the Zeek network analysis framework.  
No payload inspection or credential data is used.

---

## 3. Threat Model

The system models a remote, unauthenticated attacker attempting to gain access to services through repeated or abnormal access attempts.

The following attacker behaviors are in scope:

### 3.1 Web Brute Force
- Repeated HTTP requests to login endpoints
- High failure rate (e.g., 401 / 403 responses)
- Short inter-arrival times between requests

### 3.2 Web Scanning
- High-volume requests across many distinct URLs
- Requests for non-existent or sensitive paths
- Abnormal request diversity from a single source

### 3.3 SSH Brute Force
- Repeated SSH connection attempts from a single IP
- Short-lived failed sessions
- Unusually high connection frequency to port 22

The attacker is assumed to have no prior authentication and no internal access.

---

## 4. Assumptions

This project makes the following assumptions:

- Logs may be incomplete or noisy
- SSH authentication success or failure is inferred indirectly
- Traffic is analyzed offline, not in real time
- Encrypted payloads are not inspected
- Attacks are detected based on behavior, not signatures

These assumptions reflect the constraints of working with derived log data.

---

## 5. Detection Approach

The detection pipeline consists of four stages:

1. Log ingestion and normalization
2. Feature extraction over fixed time windows
3. Behavior detection using rules and statistical thresholds
4. Alert generation with human-readable explanations

Detection logic prioritizes **precision and interpretability** over recall.

---

## 6. Non-Goals

The following are explicitly out of scope:

- Real-time intrusion prevention
- Malware analysis or payload inspection
- Advanced machine learning models
- Enterprise-scale SIEM deployment
- Automated response or blocking

This project is intended as a **research-style prototype**, not a production system.

---

## 7. Ethical Considerations

This system is designed for educational and defensive security purposes only.

- No live systems are scanned
- All datasets are public or synthetically generated
- No personally identifiable information is intentionally collected
- Results are reported in aggregate and anonymized form

---

## 8. Evaluation Plan

The system will be evaluated using:

- Detection accuracy on labeled attack intervals
- False positive rate on benign traffic
- Qualitative analysis of alert explanations

Failure cases and limitations will be documented.

---

## 9. Limitations

- SSH authentication outcomes are inferred, not explicit
- Dataset attacks may not reflect all real-world behaviors
- Detection thresholds may not generalize across environments

These limitations are expected and acknowledged.

---

## 10. Expected Outcome

The expected outcome is an open-source framework that demonstrates how structured log data can be used to model and detect common attack behaviors in a transparent and explainable manner.