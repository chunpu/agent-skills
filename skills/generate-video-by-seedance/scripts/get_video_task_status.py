#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Poll Volcengine Ark Doubao Seedance video generation task status and
download the resulting video when it is ready.

Endpoint:

  GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional


def get_api_key(provided_key: Optional[str]) -> Optional[str]:
    if provided_key:
        return provided_key
    return os.environ.get("ARK_API_KEY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Poll Seedance video task status and download the video when ready.",
    )
    parser.add_argument(
        "task_id",
        help="Seedance video task ID, e.g. cgt-20260226184301-4h8v6.",
    )
    parser.add_argument(
        "--filename",
        "-f",
        help=(
            "Output filename (e.g. 完成视频.mp4). "
            "If not given, defaults to <task_id>.mp4 under outputs/."
        ),
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Polling interval in seconds (default: 10).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Maximum wait time in seconds before giving up (default: 600).",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Ark API key (overrides ARK_API_KEY env var).",
    )
    return parser.parse_args()


def resolve_output_path(task_id: str, filename: Optional[str]) -> Path:
    if filename:
        path = Path(filename)
    else:
        path = Path("outputs") / f"{task_id}.mp4"

    if not path.parent or str(path.parent) == ".":
        path = Path("outputs") / path.name
    if path.suffix == "":
        path = path.with_suffix(".mp4")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def download_video(url: str, output_path: Path) -> None:
    import requests

    print(f"Downloading video from: {url}")

    try:
        resp = requests.get(url, stream=True, timeout=300)
    except Exception as e:
        print(f"Error downloading video from URL: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(
            f"Error: Failed to download video, HTTP {resp.status_code}",
            file=sys.stderr,
        )
        try:
            print(resp.text, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)

    try:
        with output_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                f.write(chunk)
    except Exception as e:
        print(f"Error saving video to file: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_task(task_id: str, api_key: str) -> dict:
    import requests

    endpoint = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    resp = requests.get(endpoint, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"Ark video task API returned HTTP {resp.status_code}", file=sys.stderr)
        try:
            print(resp.text, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)

    try:
        return resp.json()
    except Exception as e:
        print(f"Failed to parse Ark video task JSON response: {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)


def extract_status_and_url(data: dict) -> tuple[str, Optional[str]]:
    status = str(data.get("status") or "").lower() or "pending"
    video_url = (
        (data.get("content") or {}).get("video_url")
        or data.get("video_url")
        or data.get("url")
    )

    if not video_url:
        d = data.get("data")
        if isinstance(d, list) and d:
            first = d[0]
            if isinstance(first, dict):
                video_url = (
                    (first.get("content") or {}).get("video_url")
                    or first.get("video_url")
                    or first.get("url")
                )
        elif isinstance(d, dict):
            video_url = (
                (d.get("content") or {}).get("video_url")
                or d.get("video_url")
                or d.get("url")
            )

    return status, video_url


def main() -> None:
    args = parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No Ark API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set ARK_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    task_id = args.task_id.strip()
    if not task_id:
        print("Error: task_id cannot be empty.", file=sys.stderr)
        sys.exit(1)

    output_path = resolve_output_path(task_id, args.filename)

    start = time.time()
    last_status: Optional[str] = None

    while True:
        elapsed = time.time() - start
        if elapsed > args.timeout:
            print(
                f"Timeout reached ({args.timeout}s). Last known status: {last_status or 'unknown'}.",
                file=sys.stderr,
            )
            sys.exit(1)

        data = fetch_task(task_id, api_key)
        status, video_url = extract_status_and_url(data)
        last_status = status

        print(f"Task {task_id} status: {status}")

        if status in ("succeeded", "success", "completed"):
            if not video_url:
                print("Task succeeded but no video_url found in response.", file=sys.stderr)
                sys.exit(1)

            download_video(video_url, output_path)
            full_path = output_path.resolve()
            print(f"\nVideo saved: {full_path}")
            print(f"MEDIA: {full_path}")
            return

        if status in ("failed", "error"):
            print("Task failed.", file=sys.stderr)
            # Print truncated raw data for debugging.
            try:
                print(str(data)[:2000], file=sys.stderr)
            except Exception:
                pass
            sys.exit(1)

        # Otherwise, keep polling.
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

