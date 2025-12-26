# LogAnalyzer

[Demo Video](https://youtu.be/9YzAtchUyn8)

## What is the problem?

Security logs are often noisy, voluminous, and difficult to interpret. Analysts need tools that can tell the story behind the logs rather than just flagging individual events. This project addresses the challenge of detecting malicious behavior in network traffic without relying on payload inspection or complex machine learning models.

## What does it do?

LogAnalyzer is a lightweight intrusion detection framework that models attacker behavior over time. It parses Zeek logs (`http.log` and `conn.log`) and detects:

- **Web Brute Force:** High volume of requests to few resources.
- **Web Scanning:** Requests to many distinct URLs.
- **SSH Brute Force:** Repeated failed connection attempts.

It normalizes events into a unified format and applies time-windowed behavioral rules to identify attacks.

## How do I run it?

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/spyduck007/LogAnalyzer.git
    cd LogAnalyzer
    ```
2.  Ensure you have Python 3 installed.
3.  (Optional) Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### Usage

The main entry point is `log_analyzer.py`.

**Web Detection:**

```bash
python log_analyzer.py web --http-log data/logs/friday/http.log --conn-log data/logs/friday/conn.log
```

**SSH Detection:**

```bash
python log_analyzer.py ssh --conn-log data/logs/thursday/conn.log
```

### Sample Output

When you run the tool, it outputs a summary of detected attack windows:

```text
=== Web Detection Results ===
Time window: 60 seconds
Web brute force windows: 32
Web scanning windows:    267

=== SSH Detection Results ===
Time window: 60 seconds
SSH brute force windows: 4
```

### Code Snippet

The core event model allows for unified analysis:

```python
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
```

For more details, check the `docs/` folder.

## Limitations & Considerations

This tool is a research prototype designed for educational purposes and offline analysis.

- **Inferred Authentication:** SSH success is inferred from connection metadata (bytes, duration), not actual login status.
- **No Payload Inspection:** It does not decrypt HTTPS or inspect packet payloads, relying solely on behavioral patterns.
- **Offline Only:** Designed for post-incident analysis of log files, not real-time stream processing.
- **Dataset Specific:** Thresholds are tuned for the CIC-IDS2017 dataset and may need adjustment for other environments.
