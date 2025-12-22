from src.pipeline.normalize import load_events
from src.detection.windows import group_events_by_window
from src.detection.web_bruteforce import detect_web_bruteforce
from src.detection.web_scanning import detect_web_scanning


def run():
    events = load_events(
        "data/logs/friday/http.log",
        "data/logs/friday/conn.log"
    )

    windows = group_events_by_window(events, window_size=60)

    alerts = []
    scan_alerts = []

    for key, window_events in windows.items():
        if detect_web_bruteforce(window_events):
            alerts.append(key)
        if detect_web_scanning(window_events):
            scan_alerts.append(key)

    print(f"Detected {len(alerts)} web brute force windows")
    print(f"Detected {len(scan_alerts)} web scanning windows")


if __name__ == "__main__":
    run()