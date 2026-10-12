#!/usr/bin/env python3
"""Reconstruct Mattermost (chat.ama.gov.pt) conversations from a decrypted trace.

Sources inside the capture, all read through tshark (read-only on the pcap):
  * websocket "posted" / "post_edited" events pushed by the server,
  * request bodies of POST /api/v4/posts (what a client sent),
  * response bodies of GET /api/v4/channels/<id>/posts (history a client loaded),
  * user and channel objects seen anywhere, to map ids to usernames.

Posts are de-duplicated by post id and printed in create_at order, with the
create_at time in UTC and the frame number where the post was first seen.

usage: mattermost_posts.py <trace.pcapng> <tls.keys> [--tsv]
"""
import json
import subprocess
import sys
from datetime import datetime, timezone


def tshark(pcap, keys, display_filter, fields):
    cmd = ["tshark", "-r", pcap, "-o", f"tls.keylog_file:{keys}",
           "-Y", display_filter, "-T", "fields", "-E", "separator=\t"]
    for f in fields:
        cmd += ["-e", f]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        yield line.split("\t")


def as_text(value):
    """http.file_data comes out hex-encoded; websocket text comes out plain."""
    value = value.strip()
    if not value:
        return ""
    try:
        return bytes.fromhex(value.replace(":", "")).decode("utf-8", "replace")
    except ValueError:
        # tshark -T fields escapes backslashes in text fields; undo that.
        return value.replace("\\\\", "\\")


def walk(obj):
    """Yield every dict nested anywhere in a JSON value."""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def loads_lenient(text):
    try:
        return json.loads(text)
    except ValueError:
        return None


def main():
    pcap, keys = sys.argv[1], sys.argv[2]
    tsv = "--tsv" in sys.argv
    users, channels, posts = {}, {}, {}

    def absorb(doc, frame, src, epoch=0.0):
        for d in walk(doc):
            # Server events wrap the post as a JSON string in data.post.
            if isinstance(d.get("post"), str):
                inner = loads_lenient(d["post"])
                if inner:
                    absorb(inner, frame, src, epoch)
            if "username" in d and "id" in d:
                users[d["id"]] = d["username"]
            if "display_name" in d and "id" in d and "type" in d and "team_id" in d:
                channels[d["id"]] = d.get("name") or d["display_name"]
            if "message" in d and "channel_id" in d and "user_id" in d and "id" in d:
                p = posts.setdefault(d["id"], dict(d, _frame=frame, _src=src, _epoch=epoch))
                if len(d.get("message", "")) > len(p.get("message", "")):
                    p.update(d)
            # Client-side POST bodies have no id/user yet: key them by pending id.
            elif "message" in d and "channel_id" in d and "pending_post_id" in d:
                key = "pending:" + d["pending_post_id"]
                posts.setdefault(key, dict(d, _frame=frame, _src=src, _epoch=epoch))

    for frame, epoch, src, payload in tshark(pcap, keys, "websocket.payload",
                                             ["frame.number", "frame.time_epoch", "ip.src",
                                              "websocket.payload.text"]):
        doc = loads_lenient(as_text(payload))
        if doc is not None:
            absorb(doc, frame, src, float(epoch))

    # Responses carry no Host header, so select both directions by the
    # Mattermost server address (10.10.20.10 also serves the intranet; absorb()
    # only keeps objects that look like users, channels or posts).
    for frame, epoch, src, body in tshark(pcap, keys, "http.file_data && ip.addr == 10.10.20.10",
                                          ["frame.number", "frame.time_epoch", "ip.src", "http.file_data"]):
        doc = loads_lenient(as_text(body))
        if doc is not None:
            absorb(doc, frame, src, float(epoch))

    # A pending post is a duplicate once the server echoed it back with an id.
    echoed = {p.get("pending_post_id") for k, p in posts.items() if not k.startswith("pending:")}
    rows = []
    for k, p in posts.items():
        if k.startswith("pending:") and p.get("pending_post_id") in echoed:
            continue
        ts = p.get("create_at") or int(p["_epoch"] * 1000)
        when = datetime.fromtimestamp(ts / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if ts else "?"
        who = users.get(p.get("user_id"), p.get("user_id", "?"))
        chan = channels.get(p.get("channel_id"), p.get("channel_id"))
        files = ",".join(p.get("file_ids") or [])
        rows.append((ts, when, p["_frame"], p["_src"], who, chan, files, p.get("message", "")))

    for ts, when, frame, src, who, chan, files, msg in sorted(rows):
        if tsv:
            print("\t".join([when, str(frame), src, who, chan, files, msg.replace("\n", " / ")]))
        else:
            extra = f" [files: {files}]" if files else ""
            print(f"{when} UTC  frame {frame}  {src}  {who} -> {chan}{extra}\n    {msg}\n")


if __name__ == "__main__":
    main()
