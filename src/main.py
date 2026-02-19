#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime

def load_data(data_file):
    default = {"current": None, "history": []}
    if not os.path.exists(data_file):
        return default
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        if (not isinstance(data, dict) or
            "current" not in data or
            "history" not in data or
            not isinstance(data["history"], list)):
            raise ValueError("Invalid data structure")
        if data["current"] is not None:
            current = data["current"]
            if (not isinstance(current, dict) or
                "name" not in current or
                "start" not in current):
                raise ValueError("Invalid current task structure")
        return data
    except Exception as e:
        print(f"Error loading data from {data_file}: {e}. Starting with fresh data.",
              file=sys.stderr)
        return default

def save_data(data, data_file):
    os.makedirs(os.path.dirname(data_file) or '.', exist_ok=True)
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def start_task(data, name, data_file):
    if data["current"]:
        stop_task(data, data_file)
    data["current"] = {"name": name, "start": datetime.now().isoformat()}
    save_data(data, data_file)
    print(f"Started timer for '{name}' at {data['current']['start']}")

def stop_task(data, data_file):
    if not data["current"]:
        print("No current task to stop.")
        return False
    start_str = data["current"]["start"]
    start = datetime.fromisoformat(start_str)
    end = datetime.now()
    duration = (end - start).total_seconds()
    entry = {
        "name": data["current"]["name"],
        "start": start_str,
        "end": end.isoformat(),
        "duration": duration
    }
    data["history"].append(entry)
    data["current"] = None
    save_data(data, data_file)
    print(f"Stopped '{entry['name']}'. Duration: {duration:.1f}s")
    return True

def list_tasks(data):
    if data["current"]:
        print("Current:")
        print(f"  {data['current']['name']} started at {data['current']['start']}")
        print()
    if data["history"]:
        print("History:")
        for entry in data["history"]:
            print(f"  {entry['name']}: {entry['start']} - {entry['end']} ({entry['duration']:.1f}s)")
    elif not data["current"]:
        print("No tasks recorded.")

def main():
    parser = argparse.ArgumentParser(description="CLI task timer")
    parser.add_argument("--version", action="version", version="task-timer 0.1.0")
    parser.add_argument("--data-file", default="task_timer.json",
                        help="Path to the JSON data file")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    start_parser = subparsers.add_parser("start", help="Start a task timer")
    start_parser.add_argument("name", help="Task name")
    stop_parser = subparsers.add_parser("stop", help="Stop current task")
    list_parser = subparsers.add_parser("list", help="List tasks")
    args = parser.parse_args()
    data_file = args.data_file
    data = load_data(data_file)
    if args.command == "start":
        start_task(data, args.name, data_file)
    elif args.command == "stop":
        if not stop_task(data, data_file):
            sys.exit(1)
    elif args.command == "list":
        list_tasks(data)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
