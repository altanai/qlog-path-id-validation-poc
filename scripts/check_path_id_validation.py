#!/usr/bin/env python3
"""Check the documented path_id validation cases without third-party modules."""

import json
from pathlib import Path

MAX_PATH_ID = (1 << 32) - 1
CASES = Path(__file__).resolve().parents[1] / "validation" / "path-id-cases.json"


def is_path_id(value):
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= MAX_PATH_ID


def validate_case(case):
    trace = case.get("trace")
    if not isinstance(trace, dict):
        return False, "trace must be an object"

    common_fields = trace.get("common_fields", {})
    if not isinstance(common_fields, dict):
        return False, "common_fields must be an object"
    if "path_id" in common_fields and not is_path_id(common_fields["path_id"]):
        return False, "common_fields.path_id must be an unsigned 32-bit integer"

    events = trace.get("events")
    if not isinstance(events, list):
        return False, "events must be an array"

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            return False, f"events[{index}] must be an object"
        if not isinstance(event.get("time"), (int, float)) or isinstance(event.get("time"), bool):
            return False, f"events[{index}].time must be numeric"
        if not isinstance(event.get("name"), str):
            return False, f"events[{index}].name must be text"
        if not isinstance(event.get("data"), dict):
            return False, f"events[{index}].data must be an object"

        event_has_path_id = "path_id" in event
        if event_has_path_id and not is_path_id(event["path_id"]):
            return False, f"events[{index}].path_id must be an unsigned 32-bit integer"

        common_has_path_id = "path_id" in common_fields
        if common_has_path_id and event_has_path_id and event["path_id"] != common_fields["path_id"]:
            return False, f"events[{index}].path_id conflicts with common_fields.path_id"

        effective_path_id = event.get("path_id", common_fields.get("path_id"))
        if case.get("path_context_known") and effective_path_id is None:
            return False, f"events[{index}] has known path context but no effective path_id"

    return True, "valid"


def main():
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures = []
    for case in data["cases"]:
        actual, reason = validate_case(case)
        expected = case["valid"]
        passed = actual == expected
        print(f"{'PASS' if passed else 'FAIL'} {case['name']}: {reason}")
        if not passed:
            failures.append(case["name"])
    if failures:
        raise SystemExit(f"{len(failures)} validation case(s) failed")
    print(f"Validated {len(data['cases'])} path_id cases")


if __name__ == "__main__":
    main()
