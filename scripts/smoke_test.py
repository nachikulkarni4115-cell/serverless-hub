"""Smoke test for the portfolio. Run from the project root:

    python scripts/smoke_test.py

Renders every page with Flask's test client, then checks that every local
link, stylesheet, script and image resolves, that every #anchor has a target,
and that unknown URLs return the custom 404 page. Exits non-zero on failure.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, PROJECTS  # noqa: E402


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.h1 = [], set(), 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append((tag, a[key]))


failures = []


def check(condition, message):
    print(("PASS  " if condition else "FAIL  ") + message)
    if not condition:
        failures.append(message)


client = app.test_client()
pages = ["/", "/healthz"] + [f"/projects/{p['slug']}" for p in PROJECTS]
checked_assets = set()

for path in pages:
    response = client.get(path)
    check(response.status_code == 200, f"GET {path} -> {response.status_code}")
    if path == "/healthz":
        continue
    html = response.get_data(as_text=True)
    parser = PageParser()
    parser.feed(html)
    check(parser.h1 == 1, f"{path} has exactly one <h1> (found {parser.h1})")
    for tag, ref in parser.refs:
        parsed = urlparse(ref)
        if parsed.scheme in ("http", "https", "mailto", "tel") or ref.startswith("//"):
            continue
        base, fragment = urldefrag(ref)
        if base:
            target = parsed.path
            if target not in checked_assets:
                checked_assets.add(target)
                r = client.get(target)
                check(r.status_code == 200, f"local reference {target} -> {r.status_code}")
            if fragment and target == "/":
                home_ids = PageParser()
                home_ids.feed(client.get("/").get_data(as_text=True))
                check(fragment in home_ids.ids, f"anchor /#{fragment} exists on the homepage")
        elif fragment:
            check(fragment in parser.ids, f"{path}: in-page anchor #{fragment} exists")

missing = client.get("/projects/does-not-exist")
check(missing.status_code == 404 and b"doesn" in missing.data, "unknown project slug returns the custom 404 page")
check(client.get("/no-such-page").status_code == 404, "unknown URL returns 404")


home_html = client.get("/").get_data(as_text=True)
check('id="bg-canvas"' in home_html, "homepage includes the canvas background")
check('class="ticker"' in home_html, "homepage includes the ticker")
check('class="stamp"' in home_html, "homepage includes the hero stamp")
check("What the projects taught me" in home_html, "homepage includes the 'what the projects taught me' block")
check(home_html.count("data-reveal") >= 10, "homepage has scroll-reveal hooks")
detail_html = client.get("/projects/voice-controlled-ai-agent").get_data(as_text=True)
check('class="toc"' in detail_html and 'id="targets"' in detail_html and 'id="next"' in detail_html,
      "project page has 'On this page', design targets and next steps")

for p in PROJECTS:
    for img in p["images"]:
        path = os.path.join(app.static_folder, "images", "projects", img["file"])
        check(os.path.isfile(path), f"project image exists: {img['file']}")

print()
if failures:
    print(f"{len(failures)} check(s) failed.")
    sys.exit(1)
print("All checks passed.")
