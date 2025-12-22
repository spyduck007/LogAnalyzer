# Lightweight Log-Based Intrusion Detection Framework

## Overview

This project is a lightweight intrusion detection framework that analyzes system and network logs to identify malicious behavior. Instead of inspecting payloads or using machine learning, the system focuses on **modeling attacker behavior over time** using interpretable rules.

The project was built as an exploration of how intrusion detection systems work in practice, especially when dealing with noisy and incomplete data.

The framework detects three types of attacks:

- Web brute force attacks
- Web scanning activity
- SSH brute force attacks

This is not intended to be a production SIEM, but a research-style prototype that emphasizes clarity and correctness.

---

## Data Sources

This project uses public network traffic from the **CIC-IDS2017** dataset.

- **Friday traffic** is used for web-based attacks
- **Thursday traffic** is used for SSH brute force attacks

Raw PCAP files are processed using the **Zeek** network analysis framework to generate structured logs. Raw PCAPs and logs are intentionally not committed to this repository.

---

## Event Model

All log entries are normalized into a unified `Event` abstraction with the following fields:

- `timestamp`
- `source_ip`
- `dest_ip`
- `protocol`
- `service`
- `action`
- `resource`
- `success`
- `bytes`

This abstraction allows HTTP and SSH activity to be analyzed using the same temporal model.

---

## Detection Approach

Events are grouped into fixed-size time windows (60 seconds) per source IP. Detection logic operates on these windows rather than on individual events.

### Web Brute Force Detection

Web brute force attacks are detected based on **request concentration**:

- A large number of HTTP requests
- Targeting a small number of resources
- Within a short time window

This approach was chosen after observing that HTTP status codes alone were unreliable indicators of failed authentication in real traffic.

---

### Web Scanning Detection

Web scanning behavior is detected based on **resource diversity**:

- A high number of distinct URLs
- Within a short time window
- Originating from a single source IP

This behavior is distinct from brute force attacks, which usually focus on a small number of endpoints.

---

### SSH Brute Force Detection

SSH brute force attacks are detected using connection-level metadata:

- Repeated SSH connection attempts
- Low success ratio
- Short-lived or low-byte connections

Authentication success is inferred from connection behavior rather than payload inspection.

---

## Results

Using conservative and explainable thresholds, the system detected:

- 32 web brute force windows
- Web scanning activity across multiple windows
- 4 SSH brute force windows

These detections represent high-confidence attack clusters rather than exhaustive detection.

---

## Limitations

- SSH authentication success is inferred indirectly
- Encrypted payloads are not inspected
- Detection thresholds are dataset-specific
- The system is designed for offline analysis only

These limitations are acknowledged as part of the design.

---

## Ethical Considerations

This project is intended for educational and defensive security research only.

- All datasets are publicly available
- No live systems are scanned
- No personally identifiable information is intentionally collected
- Results are reported in aggregate form

---

## Project Structure

```
src/
├── models/ # Event abstraction
├── parsers/ # Log parsers (HTTP and SSH)
├── pipeline/ # Event normalization
├── detection/ # Detection logic
docs/ # Design and schema documentation
```

---

## Command-Line Usage

This project includes a single command-line interface that allows users to run all detection pipelines without interacting directly with the codebase.

The CLI script is located in the project root:

```
log_analyzer.py
```

All commands should be run from the root directory of the repository.

---

### Web Attack Detection

To run detection for web brute force and web scanning activity using the default Friday dataset:

```bash
python log_analyzer.py web
```

Optional arguments:

- `--http-log` : Path to Zeek http.log
- `--conn-log` : Path to Zeek conn.log
- `--window` : Time window size in seconds (default: 60)

Example:

```bash
python log_analyzer.py web --window 120
```

### SSH Brute Force Detection

To run SSH brute force detection using the default Thursday dataset:

```bash
python log_analyzer.py ssh
```

Optional arguments:

- `--conn-log` : Path to Zeek conn.log
- `--window` : Time window size in seconds (default: 60)

Example:

```bash
python log_analyzer.py ssh --window 120
```

### Help

To view all available commands and options:

```bash
python log_analyzer.py --help
```

---

## Motivation

This project was built to better understand how intrusion detection systems reason about behavior when working with imperfect data. Throughout the project, the focus was on making design decisions explicit, testing assumptions against real traffic, and prioritizing interpretability over complexity.

---

## License

This project is released for educational and research purposes.
