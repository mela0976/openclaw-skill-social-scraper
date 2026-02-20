#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic Notion page writer for social media posts.
Reads JSON from stdin, writes to a Notion database.

Usage:
    echo '[{"h":"ec.wife","code":"ABC123","ts":1770000000,"text":"Hello","likes":10,"comments":2,"type":1}]' | \
    python3 notion_writer.py --platform Instagram

Environment:
    NOTION_API_KEY - Notion integration API key
    NOTION_DB_ID   - Target database ID
"""

import urllib.request
import json
import sys
import time
import os
import argparse
from datetime import datetime, timezone

# Config
API_KEY = os.environ.get("NOTION_API_KEY", "")
DB_ID = os.environ.get("NOTION_DB_ID", "")

TYPE_MAP = {1: "圖片", 2: "影片", 8: "輪播"}
PLATFORM_URL_MAP = {
    "Instagram": lambda h, code: f"https://www.instagram.com/p/{code}/",
    "Threads": lambda h, code: f"https://www.threads.com/@{h}/post/{code}",
    "Facebook": lambda h, code: code,  # FB uses full URL as code
}


def write_post(post, platform="Instagram"):
    """Write a single post to Notion."""
    # Handle timestamp formats
    if "ts" in post:
        dt = datetime.fromtimestamp(post["ts"], tz=timezone.utc).strftime("%Y-%m-%d")
    elif "time" in post:
        dt = post["time"][:10]
    else:
        dt = datetime.now().strftime("%Y-%m-%d")

    handle = post.get("h", post.get("handle", ""))
    code = post.get("code", "")
    title = (post.get("text", "") or "(無文字)")[:100]
    url_fn = PLATFORM_URL_MAP.get(platform, PLATFORM_URL_MAP["Instagram"])
    post_url = url_fn(handle, code)

    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "貼文內容": {"title": [{"text": {"content": title}}]},
            "帳號": {"select": {"name": "@" + handle}},
            "平台": {"select": {"name": platform}},
            "發布日期": {"date": {"start": dt}},
            "貼文連結": {"url": post_url},
            "讚數": {"number": post.get("likes", 0)},
            "留言數": {"number": post.get("comments", 0)},
            "類型": {"select": {"name": TYPE_MAP.get(post.get("type", 0), "文字")}},
        },
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
    )
    urllib.request.urlopen(req, timeout=10)


def main():
    parser = argparse.ArgumentParser(description="Write social media posts to Notion")
    parser.add_argument("--platform", default="Instagram", choices=["Instagram", "Threads", "Facebook"])
    parser.add_argument("--delay", type=float, default=0.35, help="Delay between writes (seconds)")
    parser.add_argument("--db", default="", help="Notion database ID (overrides env)")
    parser.add_argument("--key", default="", help="Notion API key (overrides env)")
    args = parser.parse_args()

    global API_KEY, DB_ID
    if args.key:
        API_KEY = args.key
    if args.db:
        DB_ID = args.db

    if not API_KEY or not DB_ID:
        print("Error: Set NOTION_API_KEY and NOTION_DB_ID env vars, or use --key and --db", file=sys.stderr)
        sys.exit(1)

    posts = json.load(sys.stdin)
    success = 0
    errors = 0

    for i, post in enumerate(posts):
        try:
            write_post(post, args.platform)
            success += 1
        except Exception as e:
            errors += 1
            print(f"ERR @{post.get('h', '?')}/{post.get('code', '?')}: {e}", file=sys.stderr)

        if (i + 1) % 10 == 0:
            print(f"Progress: {i+1}/{len(posts)} ({success} ok, {errors} err)")

        time.sleep(args.delay)

    print(f"\n✅ Done: {success}/{len(posts)} written to Notion ({args.platform}), {errors} errors")


if __name__ == "__main__":
    main()
