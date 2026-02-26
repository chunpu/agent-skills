#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Generate videos using Volcengine Ark Doubao Seedance video generation API.

This is a thin CLI wrapper around:

  POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks

The request / response semantics roughly mirror the TypeScript example in
`generate-video.ts` (Seedance), but with a Python + CLI interface suitable
for OpenClaw skills.
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path
from typing import List, Optional


def get_api_key(provided_key: Optional[str]) -> Optional[str]:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("ARK_API_KEY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate videos using Volcengine Ark Doubao Seedance",
    )
    parser.add_argument(
        "--prompt",
        "-p",
        help="Video generation / editing prompt (e.g. 在草地上奔跑的小狗，电影感).",
    )
    parser.add_argument(
        "--filename",
        "-f",
        required=True,
        help=(
            "Output filename (e.g. 奔跑小狗.mp4). "
            "If no directory is given, it will be saved under outputs/."
        ),
    )
    parser.add_argument(
        "--image",
        "-i",
        action="append",
        dest="images",
        metavar="IMAGE",
        help=(
            "Reference image(s) as URL or local path. "
            "URLs are sent directly; local files are encoded as data URLs. "
            "Can be specified multiple times."
        ),
    )
    parser.add_argument(
        "--ratio",
        default="16:9",
        help='Aspect ratio for the video, e.g. "16:9" (default), "9:16", "1:1", "21:9".',
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Video duration in seconds (default: 5).",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Ark API key (overrides ARK_API_KEY env var).",
    )
    parser.add_argument(
        "--model",
        help=(
            "Advanced: override Ark Seedance endpoint / model name. "
            "If not provided, a default Seedance endpoint will be used."
        ),
    )
    return parser.parse_args()


def build_image_list(images: Optional[List[str]]) -> List[str]:
    if not images:
        return []

    resolved: List[str] = []
    for item in images:
        if not item:
            continue
        item = item.strip()
        if not item:
            continue

        # If already data URL or http(s) URL, pass through.
        if item.startswith("data:") or item.startswith("http://") or item.startswith("https://"):
            resolved.append(item)
            continue

        # Otherwise, assume local file path → data URL (Base64).
        path = Path(item)
        if not path.is_file():
            print(f"Error: image path does not exist or is not a file: {item}", file=sys.stderr)
            sys.exit(1)

        ext = path.suffix.lower().lstrip(".")
        if ext in ("jpg", "jpeg"):
            fmt = "jpeg"
        elif ext in ("png", "webp"):
            fmt = ext
        else:
            fmt = ext or "jpeg"
            print(
                f"Warning: unrecognised image extension for '{item}', using '{fmt}' in data URL.",
                file=sys.stderr,
            )

        with path.open("rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        data_url = f"data:image/{fmt};base64,{b64}"
        resolved.append(data_url)

    return resolved


def build_content(prompt: Optional[str], images: List[str], model_name: str) -> List[dict]:
    content: List[dict] = []

    text_prompt = (prompt or "").strip()
    if text_prompt:
        content.append({"type": "text", "text": text_prompt})

    # 模型相关的图片策略：
    # - lite i2v 模型（如 doubao-seedance-1-0-lite-i2v-250428）支持多张 reference_image，
    #   role 字段与官方示例一致，放在 image_url 同级。
    # - 其他 pro 系列模型目前只接受 1 张 image content，多张会直接 400。
    is_lite_i2v = "lite-i2v" in (model_name or "")

    if is_lite_i2v:
        # 多图：全部作为 reference_image。
        for img in images or []:
            if not img:
                continue
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img,
                    },
                    "role": "reference_image",
                }
            )
    else:
        if images:
            first = images[0]
            if len(images) > 1:
                print(
                    f"Warning: current model '{model_name}' only supports one image; "
                    f"got {len(images)}, using the first one.",
                    file=sys.stderr,
                )
            if first:
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": first,
                        },
                    }
                )

    return content


def resolve_output_path(filename: str) -> Path:
    output_path = Path(filename)
    if not output_path.parent or str(output_path.parent) == ".":
        output_path = Path("outputs") / output_path.name
    if output_path.suffix == "":
        # Default to mp4 for video.
        output_path = output_path.with_suffix(".mp4")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


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


def main() -> None:
    args = parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No Ark API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set ARK_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # If neither prompt nor image is provided, reject early.
    if not args.prompt and not args.images:
        print("Error: prompt and reference images cannot both be empty.", file=sys.stderr)
        print("Provide at least one of: --prompt or -i/--image.", file=sys.stderr)
        sys.exit(1)

    # Import requests lazily so CLI help is fast even without dependency.
    import requests

    endpoint = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

    # Resolve model: explicit --model wins; otherwise use Seedance 1.5 pro by default.
    model_name = args.model or "doubao-seedance-1-5-pro-251215"

    images = build_image_list(args.images)
    content = build_content(args.prompt, images, model_name)

    if not content:
        print("Error: failed to build Seedance input content (empty).", file=sys.stderr)
        sys.exit(1)

    payload: dict = {
        "model": model_name,
        "content": content,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": False,
        # generate_audio can be added later if needed / supported.
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"Calling Ark Seedance video API with model={model_name}, ratio={args.ratio}, duration={args.duration}s...")
    if images:
        print(f"Using {len(images)} reference image(s) (URLs and/or local files).")

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    except Exception as e:
        print(f"Error calling Ark video API: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"Ark video API returned HTTP {resp.status_code}", file=sys.stderr)
        try:
            print(resp.text, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)

    try:
        data = resp.json()
    except Exception as e:
        print(f"Failed to parse Ark video API JSON response: {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    # Seedance task API is typically async. We try to be generous in what we accept:
    # - Prefer id / task_id as the task identifier.
    # - Try several locations for video_url-like fields.
    task_id = data.get("id") or data.get("task_id")
    video_url = (
        (data.get("content") or {}).get("video_url")
        or data.get("video_url")
        or data.get("url")
    )

    if task_id:
        print(f"Seedance video task created, task_id={task_id}")

    # Some deployments may return data: [...] wrapping task info or URLs.
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

    if not video_url:
        print("No immediate video_url in response; task is likely still processing.", file=sys.stderr)
        print("Raw response (truncated):", file=sys.stderr)
        try:
            print(str(data)[:2000], file=sys.stderr)
        except Exception:
            pass
        # Still exit 0 so callers can parse task_id from stdout.
        if task_id:
            print(f"TASK_ID: {task_id}")
        return

    output_path = resolve_output_path(args.filename)
    download_video(video_url, output_path)

    full_path = output_path.resolve()
    print(f"\nVideo saved: {full_path}")
    # OpenClaw parses MEDIA tokens and will attach the file on supported providers.
    print(f"MEDIA: {full_path}")


if __name__ == "__main__":
    main()

