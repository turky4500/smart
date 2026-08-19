# -*- coding: utf-8 -*-
"""Daily hook used by GitHub Actions.

Auto-publishing recycled AdSense/SEO templates hurt site quality.
This script now refuses to create a new post unless there is an unused
draft in scripts/drafts.json. Otherwise it exits successfully so the
workflow can still refresh the sitemap.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DRAFTS = os.path.join(os.path.dirname(__file__), "drafts.json")


def main():
    if not os.path.exists(DRAFTS):
        print("No drafts.json found. Skipping new article to protect content quality.")
        return 0

    with open(DRAFTS, encoding="utf-8") as f:
        data = json.load(f)

    unused = [d for d in data.get("articles", []) if not d.get("published")]
    if not unused:
        print("No unused editorial drafts. Skipping new article.")
        return 0

    print("Unused drafts exist, but publishing is manual. Mark one published after review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
