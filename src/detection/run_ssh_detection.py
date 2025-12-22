from src.parsers.conn_parser import parse_conn_log
from src.detection.windows import group_events_by_window
from src.detection.ssh_bruteforce import detect_ssh_bruteforce

def run():
    ssh_events = parse_conn_log("data/logs/thursday/conn.log")

    windows = group_events_by_window(ssh_events, window_size=60)

    alerts = []

    for key, events in windows.items():
        if detect_ssh_bruteforce(events):
            alerts.append(key)

    print(f"Detected {len(alerts)} SSH brute force windows")


if __name__ == "__main__":
    run()
