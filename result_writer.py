#!/usr/bin/python3

"""Very small result writer used by the historical test harness sample."""

import json
from datetime import datetime
from pathlib import Path


class ResultWriter:
    def __init__(self, report_file: str, log_to_syslog: bool = False):
        self._report_file = Path(report_file)
        self._log_to_syslog = log_to_syslog

    def add_test_entry(self, description: str, success: bool, duration) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "description": description,
            "success": bool(success),
            "duration_seconds": duration.total_seconds()
            if hasattr(duration, "total_seconds")
            else float(duration),
        }
        with self._report_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
