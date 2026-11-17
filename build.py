#!/usr/bin/env python3
"""Assembles the static pages: shared head, nav and footer around each page body in src/.

Run `python3 build.py` after editing anything in src/ or this file, then commit both
the src/ file and the generated root .html file. Vercel serves the root files as they are.
Shared blocks used by more than one page live in src/partials/ and are pulled in with
{{> name}}.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
PARTIALS = SRC / "partials"
SITE = "https://resourceramp.co"
ASSET_VERSION = "20261117b"

NAV_ITEMS = [
    ("founders", "/founders", "For founders"),
    ("investors", "/investors", "For investors"),
    ("corporates", "/corporates", "For corporates"),
    ("hub", "/hub", "The hub"),
    ("events", "/events", "Events"),
    ("about", "/about", "About"),
]

NAV = """
<a class="skip" href="#main">Skip to content</a>
<header class="nav" id="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Resource Ramp home"><img src="/img/logo.png" alt="Resource Ramp" width="194" height="30"></a>
    <nav aria-label="Main">
      <ul class="nav-links" id="menu">
{links}
        <li class="nav-apply"><a href="/apply" {a_apply}>Apply for Cohort 1</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-primary btn-sm" href="/apply">Apply for Cohort 1</a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="/img/logo-white.png" alt="Resource Ramp" width="181" height="28">
        <p class="tag">LAUNCH &middot; GROW &middot; THRIVE</p>
        <p class="footer-desc">A startup incubation centre in Mumbai, and an initiative of Resource Workspaces.</p>
        <p class="footer-group"><span>Group companies</span><a href="https://www.resource.bz/" rel="noopener" target="_blank"><img src="/img/resource-wordmark.png" alt="Resource" height="14"></a><a href="https://www.resourcespaces.com/" rel="noopener" target="_blank"><img src="/img/resource-workspaces.png" alt="Resource Workspaces" height="30"></a><a class="logo-tile" href="https://www.sabari.co/" rel="noopener" target="_blank"><img src="/img/sabari-group.png" alt="Sabari Group, Building Realties since 1990" height="30"></a></p>
      </div>
      <div>
        <h2 class="fh">Programme</h2>
        <ul>
          <li><a href="/founders">For founders</a></li>
          <li><a href="/founders#journey">How to apply</a></li>
          <li><a href="/#faq">Questions and answers</a></li>
          <li><a href="/apply">Apply for Cohort 1</a></li>
        </ul>
      </div>
      <div>
        <h2 class="fh">Resource Ramp</h2>
        <ul>
          <li><a href="/investors">For investors</a></li>
          <li><a href="/corporates">For corporates</a></li>
          <li><a href="/hub">The hub</a></li>
          <li><a href="/events">Events</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </div>
      <div>
        <h2 class="fh">Contact</h2>
        <address>
          <a href="mailto:ramp@resource.bz">ramp@resource.bz</a><br>
          101-103, Ujagar Chambers,<br>7 V. N. Purav Marg, Deonar,<br>Mumbai 400088, India
        </address>
        <ul class="footer-ext">
          <li><a href="https://maps.app.goo.gl/9EXsXJCVToM4Vr5s8" rel="noopener" target="_blank">Open in Google Maps</a></li>
          <li><a href="https://www.linkedin.com/company/resourceramp/" rel="noopener" target="_blank">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <p class="statutory">Resource Ramp Private Limited &middot; CIN U70200MH2026PTC473696 &middot; Registered office: 101-103, Ujagar Chambers, 7 V. N. Purav Marg, Deonar, Mumbai 400088 &middot; ramp@resource.bz<br>&copy; 2026 Resource Ramp Private Limited. All rights reserved.</p>
      <p><a href="/privacy-policy">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="/terms-of-use">Terms of use</a> &nbsp;&middot;&nbsp; <a href="/disclaimer">Disclaimer</a></p>
    </div>
  </div>
</footer>
<dialog class="lightbox" id="lightbox" aria-label="Photograph">
  <button class="lb-close" type="button" aria-label="Close">
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <button class="lb-nav lb-prev" type="button" aria-label="Previous photograph">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
  </button>
  <figure><img alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><figcaption></figcaption></figure>
  <button class="lb-nav lb-next" type="button" aria-label="Next photograph">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
  </button>
</dialog>
<script src="/main.js?v={v}" defer></script>
"""

HEAD = """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Resource Ramp">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/png" sizes="32x32" href="/img/icon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/img/icon-512.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css?v={v}">
{extra_head}
</head>
<body>
"""

TAIL = "</body>\n</html>\n"


def include_partials(text):
    def repl(m):
        return (PARTIALS / f"{m.group(1)}.html").read_text().rstrip("\n")
    return re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", repl, text)


def build():
    for path in sorted(SRC.glob("*.html")):
        text = path.read_text()
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        meta = dict(line.split(":", 1) for line in m.group(1).splitlines())
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        body = include_partials(m.group(2))
        slug = path.stem
        canonical = SITE + ("/" if slug == "index" else f"/{slug}")
        active = meta.get("active", "")
        links = "\n".join(
            '        <li><a href="%s"%s>%s</a></li>' % (href, ' aria-current="page"' if key == active else "", label)
            for key, href, label in NAV_ITEMS
        )
        nav = NAV.replace("{links}", links).replace("{a_apply}", 'aria-current="page"' if active == "apply" else "")
        head = HEAD.format(title=meta["title"], description=meta["description"], canonical=canonical,
                           site=SITE, extra_head=meta.get("extra_head", ""), v=ASSET_VERSION)
        (ROOT / f"{slug}.html").write_text(head + nav + body + FOOTER.replace("{v}", ASSET_VERSION) + TAIL)
        print("built", slug)


if __name__ == "__main__":
    build()
