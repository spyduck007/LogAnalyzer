#!/usr/bin/env python3

import argparse
from src.pipeline.normalize import load_events
from src.detection.windows import group_events_by_window
from src.detection.web_bruteforce import detect_web_bruteforce
from src.detection.web_scanning import detect_web_scanning
from src.parsers.conn_parser import parse_conn_log
from src.detection.ssh_bruteforce import detect_ssh_bruteforce


def run_web_detection(http_log: str, conn_log: str, window: int):
    events = load_events(http_log, conn_log)
    windows = group_events_by_window(events, window)

    brute_force = 0
    scanning = 0

    for events_in_window in windows.values():
        if detect_web_bruteforce(events_in_window):
            brute_force += 1
        if detect_web_scanning(events_in_window):
            scanning += 1

    print("=== Web Detection Results ===")
    print(f"Time window: {window} seconds")
    print(f"Web brute force windows: {brute_force}")
    print(f"Web scanning windows:    {scanning}")


def run_ssh_detection(conn_log: str, window: int):
    ssh_events = parse_conn_log(conn_log)
    windows = group_events_by_window(ssh_events, window)

    ssh_brute = sum(
        1
        for events_in_window in windows.values()
        if detect_ssh_bruteforce(events_in_window)
    )

    print("=== SSH Detection Results ===")
    print(f"Time window: {window} seconds")
    print(f"SSH brute force windows: {ssh_brute}")


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight Log-Based Intrusion Detection Framework"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- Web detection ----
    web_parser = subparsers.add_parser(
        "web", help="Run web brute force and scanning detection"
    )
    web_parser.add_argument(
        "--http-log", default="data/logs/friday/http.log", help="Path to Zeek http.log"
    )
    web_parser.add_argument(
        "--conn-log", default="data/logs/friday/conn.log", help="Path to Zeek conn.log"
    )
    web_parser.add_argument(
        "--window",
        type=int,
        default=60,
        help="Time window size in seconds (default: 60)",
    )

    # ---- SSH detection ----
    ssh_parser = subparsers.add_parser("ssh", help="Run SSH brute force detection")
    ssh_parser.add_argument(
        "--conn-log",
        default="data/logs/thursday/conn.log",
        help="Path to Zeek conn.log (Thursday data)",
    )
    ssh_parser.add_argument(
        "--window",
        type=int,
        default=60,
        help="Time window size in seconds (default: 60)",
    )

    args = parser.parse_args()

    if args.command == "web":
        run_web_detection(args.http_log, args.conn_log, args.window)
    elif args.command == "ssh":
        run_ssh_detection(args.conn_log, args.window)


if __name__ == "__main__":
    main()
