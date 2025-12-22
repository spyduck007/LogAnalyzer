from src.pipeline.normalize import load_events
from src.detection.windows import group_events_by_window
from src.detection.web_bruteforce import detect_web_bruteforce
from src.detection.web_scanning import detect_web_scanning
from src.parsers.conn_parser import parse_conn_log
from src.detection.ssh_bruteforce import detect_ssh_bruteforce


def run():
    events = load_events(
        "data/logs/friday/http.log",
        "data/logs/thursday/conn.log"
    )

    windows = group_events_by_window(events, window_size=60)

    brute_force = 0
    scanning = 0

    for w in windows.values():
        if detect_web_bruteforce(w):
            brute_force += 1
        if detect_web_scanning(w):
            scanning += 1

    ssh_events = parse_conn_log("data/logs/thursday/conn.log")
    ssh_windows = group_events_by_window(ssh_events, window_size=60)

    ssh_brute = sum(
        1 for w in ssh_windows.values()
        if detect_ssh_bruteforce(w)
    )

    print("=== Detection Summary ===")
    print(f"Web brute force windows: {brute_force}")
    print(f"Web scanning windows:    {scanning}")
    print(f"SSH brute force windows: {ssh_brute}")


if __name__ == "__main__":
    run()
