# task-timer

A simple, production-ready CLI task timer built with Python's standard library. It allows users to start and stop timers for tasks, automatically stopping any running task on restart, and lists current and historical task durations. Data is persistently stored in a JSON file with robust loading/validation and fallback to fresh data on errors, ensuring clean UX without tracebacks.

## Installation

bash
git clone https://github.com/yourusername/task-timer.git
cd task-timer
No external dependencies; uses Python standard library only. Make executable (optional):

bash
chmod +x src/main.py
Run with `python src/main.py` or `./src/main.py`.

## Usage

Basic commands (default data file: `task_timer.json`):

bash
# Show help
python src/main.py --help

# Start timer for a task (auto-stops previous if running)
python src/main.py start "Write report"

# Stop current task
python src/main.py stop

# List current task and history
python src/main.py list
Additional options:
- `--data-file PATH`: Custom JSON data file (default: `task_timer.json`)
- `--version`: Show version (0.1.0)

## Features

- Subcommands: `start <name>`, `stop`, `list`
- Auto-stop previous task on new start
- Persistent JSON storage with structure validation and error recovery
- Duration calculation in seconds
- Clean console output for current task and full history
- No external dependencies; robust and fault-tolerant

## Dependencies

Python standard library only (argparse, json, os, sys, datetime).

## Tests

No tests implemented.

## License

MIT