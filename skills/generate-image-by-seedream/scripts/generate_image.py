#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Generate images using Volcengine Ark Doubao Seedream 5.0 image generation API.

This is a wrapper around:
  POST https://ark.cn-beijing.volces.com/api/v3/images/generations

Example (equivalent to the curl you provided):

    uv run generate_image.py \
      --prompt "将图1的服装换为图2的服装" \
      --filename "output.png" \
      -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
      -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
      --size 2K
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional


VERSION_TO_MODEL = {
    "4.0": "doubao-seedream-4-0-250828",
    "4.5": "doubao-seedream-4-5-251128",
    "5.0": "doubao-seedream-5-0-260128",
    # Lite variants (for advanced users)
    "4.5-lite": "doubao-seedream-4-5-251128",  # if a dedicated lite ID appears later, update here
    "5.0-lite": "doubao-seedream-5-0-lite-260128",
}

ALLOWED_SIZES_BY_VERSION = {
    "4.0": {"1K", "2K", "4K"},
    "4.5": {"2K", "4K"},
    "5.0": {"2K", "3K"},
}


def get_api_key(provided_key: Optional[str]) -> Optional[str]:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("ARK_API_KEY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images using Volcengine Ark Doubao Seedream 5.0",
    )
    parser.add_argument(
        "--prompt",
        "-p",
        required=True,
        help="Image generation/editing prompt (e.g. 将图1的服装换为图2的服装)",
    )
    parser.add_argument(
        "--filename",
        "-f",
        required=True,
        help="Output filename (JPEG by default, e.g. 可爱小狗.jpg). If no directory is given, it will be saved under outputs/.",
    )
    parser.add_argument(
        "--image-url",
        "-i",
        action="append",
        dest="image_urls",
        metavar="URL",
        help="Reference image URL(s). Can be specified multiple times.",
    )
    parser.add_argument(
        "--size",
        "-s",
        default="2K",
        help='Output size sent to Ark, e.g. "2K" (default) or "4K".',
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Ark API key (overrides ARK_API_KEY env var).",
    )
    parser.add_argument(
        "--version",
        "-v",
        choices=["4.0", "4.5", "5.0"],
        default="4.5",
        help="Seedream version: 4.0, 4.5 (default), or 5.0. Internally mapped to Ark model IDs.",
    )
    parser.add_argument(
        "--model",
        help="Advanced: override full Ark model name (e.g. doubao-seedream-4-5-251128). "
        "If provided, this takes precedence over --version.",
    )
    return parser.parse_args()


def build_payload(
    model: str,
    prompt: str,
    image_urls: Optional[List[str]],
    size: str,
) -> dict:
    payload: dict = {
        "model": model,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "size": size,
        "watermark": False,
        # We rely on the default URL-based response; do not send output_format.
    }
    if image_urls:
        payload["image"] = image_urls
    return payload


def main() -> None:
    args = parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No Ark API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set ARK_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import requests lazily so CLI help is fast even without dependency.
    import requests

    endpoint = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

    # Resolve model: explicit --model wins; otherwise map from --version.
    if args.model:
        model_name = args.model
    else:
        model_name = VERSION_TO_MODEL.get(args.version)
        if not model_name:
            print(
                f"Error: Unsupported Seedream version '{args.version}'. "
                f"Supported versions: {', '.join(sorted(VERSION_TO_MODEL.keys()))}",
                file=sys.stderr,
            )
            sys.exit(1)

    # Validate size against version constraints (only for known 4.0/4.5/5.0).
    allowed_sizes = ALLOWED_SIZES_BY_VERSION.get(args.version)
    if allowed_sizes is not None and args.size not in allowed_sizes:
        print(
            f"Error: size '{args.size}' is not supported for Seedream {args.version}. "
            f"Allowed sizes for {args.version}: {', '.join(sorted(allowed_sizes))}.",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = build_payload(
        model=model_name,
        prompt=args.prompt,
        image_urls=args.image_urls,
        size=args.size,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"Calling Ark Seedream API with model={model_name}, size={args.size}...")
    if args.image_urls:
        print(f"Using {len(args.image_urls)} reference image URL(s).")

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    except Exception as e:
        print(f"Error calling Ark API: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"Ark API returned HTTP {resp.status_code}", file=sys.stderr)
        try:
            print(resp.text, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)

    try:
        data = resp.json()
    except Exception as e:
        print(f"Failed to parse Ark API JSON response: {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    # Expected format (from Ark docs):
    # {
    #   "model": "...",
    #   "created": ...,
    #   "data": [
    #     {
    #       "url": "https://...",
    #       "size": "3136x1344"
    #     }
    #   ],
    #   "usage": { ... }
    # }
    images = data.get("data") or []
    if not images:
        print("Error: Ark API returned no images in `data`.", file=sys.stderr)
        print(data, file=sys.stderr)
        sys.exit(1)

    first = images[0]
    img_url = first.get("url")
    if not img_url:
        print("Error: First image in `data` has no `url` field.", file=sys.stderr)
        print(first, file=sys.stderr)
        sys.exit(1)

    print(f"Downloading image from: {img_url}")

    try:
        download_resp = requests.get(img_url, stream=True, timeout=120)
    except Exception as e:
        print(f"Error downloading image from URL: {e}", file=sys.stderr)
        sys.exit(1)

    if download_resp.status_code != 200:
        print(
            f"Error: Failed to download image, HTTP {download_resp.status_code}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Ark 默认返回 JPEG。
    # 1) 如果用户没带后缀，就默认补上 .jpg
    # 2) 如果用户没指定目录（纯文件名），默认写入 outputs/ 目录
    output_path = Path(args.filename)
    if not output_path.parent or str(output_path.parent) == ".":
        output_path = Path("outputs") / output_path.name
    if output_path.suffix == "":
        output_path = output_path.with_suffix(".jpg")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "wb") as f:
            for chunk in download_resp.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                f.write(chunk)
    except Exception as e:
        print(f"Error saving image to file: {e}", file=sys.stderr)
        sys.exit(1)

    full_path = output_path.resolve()
    print(f"\nImage saved: {full_path}")
    # OpenClaw parses MEDIA tokens and will attach the file on supported providers.
    print(f"MEDIA: {full_path}")


if __name__ == "__main__":
    main()

