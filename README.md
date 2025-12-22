# Lightweight Log-Based Intrusion Detection Framework

## Overview

This project implements a lightweight, explainable intrusion detection framework that identifies malicious behavior from system and network logs. Rather than relying on payload inspection or black-box machine learning, the system models **attacker behavior over time** using interpretable rules applied to structured log events.

The framework detects three common attack behaviors:
- Web brute force attacks
- Web scanning activity
- SSH brute force attacks

The goal of this project is not to build a production SIEM, but to explore how heterogeneous logs can be normalized into a unified event model and analyzed using transparent detection logic.

---

## Data Sources

This project uses publicly available network traffic from the **CIC-IDS2017** dataset.

- **Friday traffic** is used for web-based attacks
- **Thursday traffic** is used for SSH brute force behavior

Raw PCAP files are processed using the **Zeek** network analysis framework to extract structured logs. No raw PCAPs or logs are committed to this repository.

---

## Event Abstraction

All log entries are mapped into a unified `Event` abstraction with the following fields:

- `timestamp`
- `source_ip`
- `dest_ip`
- `protocol`
- `service`
- `action`
- `resource`
- `success`
- `bytes`

This abstraction allows different protocols (HTTP and SSH) to be analyzed using a common temporal and behavioral model.

---

## Detection Approach

Events are grouped into fixed-size time windows (60 seconds) per source IP. Detection logic operates on these windows rather than on individual events.

### Web Brute Force Detection

Web brute force attacks are detected based on **request concentration**:
- A high number of HTTP requests
- Targeting a small number of resources
- Within a short time window

This approach was chosen after observing that HTTP status codes alone were unreliable indicators of authentication failure in real traffic.

---

### Web Scanning Detection

Web scanning activity is detected based on **resource diversity**:
- A high number of distinct URLs
- Within a short time window
- Originating from a single source IP

This behavior is distinct from brute force attacks, which typically focus on a small set of endpoints.

---

### SSH Brute Force Detection

SSH brute force attacks are detected using connection-level behavior:
- Repeated SSH connection attempts
- Low success ratio
- Short-lived or low-byte sessions

Authentication success is inferred from connection metadata rather than payload inspection.

---

## Results

Using conservative, interpretable thresholds, the system detected:

- 32 web brute force windows
- Web scanning activity across multiple windows
- 4 SSH brute force windows

These results reflect high-confidence attack clusters rather than exhaustive detection.

---

## Limitations

- SSH authentication success is inferred indirectly
- Encrypted payloads are not inspected
- Detection thresholds are dataset-specific
- This system is designed for offline analysis, not real-time deployment

These limitations are acknowledged and documented as part of the design.

---

## Ethical Considerations

This project is intended solely for educational and defensive security research.

- All data sources are public
- No live systems are scanned
- No personally identifiable information is intentionally collected
- Results are reported in aggregate form

---

## Project Structure

src/.  
├── models/ # Event abstraction.  
├── parsers/ # Log parsers (HTTP, SSH)  
├── pipeline/ # Event normalization   
├── detection/ # Detection logic.  
docs/ # Design and schema documentation. 


---

## Motivation

This project was built to explore how intrusion detection systems reason about behavior under real-world constraints, including noisy data, incomplete signals, and the tradeoff between precision and recall. The emphasis throughout the project is on **clarity, correctness, and explainability** rather than scale or automation.

---

## License

This project is released for educational and research purposes.