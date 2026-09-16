#!/usr/bin/env python3
"""Assembles the static pages: shared head, nav and footer around each page body in src/."""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
SITE = "https://resourceramp.co"

NAV = """
<header class="nav" id="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Resource Ramp home"><img src="/img/logo.png" alt="Resource Ramp" width="194" height="30"></a>
    <nav aria-label="Main">
      <ul class="nav-links" id="menu">
        <li><a href="/#programme" {a_programme}>Programme</a></li>
        <li><a href="/#hub" {a_hub}>The hub</a></li>
        <li><a href="/partners" {a_partners}>Corporates &amp; investors</a></li>
        <li><a href="/apply" {a_apply}>Apply</a></li>
        <li><a href="/#contact" {a_contact}>Contact</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-primary" href="/apply">Apply for Cohort 1</a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <img src="/img/logo-white.png" alt="Resource Ramp" width="181" height="28">
        <p class="tag">LAUNCH &middot; GROW &middot; THRIVE</p>
        <p style="margin-top:16px;max-width:38ch;color:#9CA3AF">A startup incubation centre in Chembur, Mumbai, and an initiative of Resource Workspaces.</p>
        <p class="footer-group"><span>Group companies</span><a href="https://www.resource.bz/" rel="noopener" target="_blank"><img src="/img/resource-wordmark.png" alt="Resource" height="14"></a><a href="https://www.resourcespaces.com/" rel="noopener" target="_blank"><img src="/img/resource-workspaces.png" alt="Resource Workspaces" height="30"></a><a class="logo-tile" href="https://www.sabari.co/" rel="noopener" target="_blank"><img src="/img/sabari-group.png" alt="Sabari Group, Building Realties since 1990" height="30"></a></p>
      </div>
      <div>
        <h3 class="fh">Resource Ramp</h3>
        <ul>
          <li><a href="/#programme">The programme</a></li>
          <li><a href="/#hub">The hub</a></li>
          <li><a href="/partners">Corporates and investors</a></li>
          <li><a href="/apply">Apply for Cohort 1</a></li>
          <li><a href="https://www.linkedin.com/company/resourceramp/" rel="noopener" target="_blank">LinkedIn</a></li>
        </ul>
      </div>
      <div>
        <h3 class="fh">Contact</h3>
        <address>
          <a href="mailto:ramp@resource.bz">ramp@resource.bz</a><br>
          101-103, Ujagar Chambers,<br>7 V. N. Purav Marg, Deonar,<br>Mumbai 400088, India
        </address>
      </div>
    </div>
    <div class="footer-legal">
      <p class="statutory">Resource Ramp Private Limited &middot; CIN U70200MH2026PTC473696 &middot; Registered office: 101-103, Ujagar Chambers, 7 V. N. Purav Marg, Deonar, Mumbai 400088 &middot; ramp@resource.bz<br>&copy; 2026 Resource Ramp Private Limited. All rights reserved.</p>
      <p><a href="/privacy-policy">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="/terms-of-use">Terms of use</a> &nbsp;&middot;&nbsp; <a href="/disclaimer">Disclaimer</a></p>
    </div>
  </div>
</footer>
<script src="/main.js" defer></script>
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
<link rel="icon" type="image/png" sizes="32x32" href="/img/icon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/img/icon-512.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/styles.css">
{extra_head}
</head>
<body>
"""

TAIL = "</body>\n</html>\n"


def build():
    for path in sorted(SRC.glob("*.html")):
        text = path.read_text()
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        meta = dict(line.split(":", 1) for line in m.group(1).splitlines())
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        body = m.group(2)
        slug = path.stem
        canonical = SITE + ("/" if slug == "index" else f"/{slug}")
        active = meta.get("active", "")
        nav = NAV
        for key in ["programme", "hub", "partners", "apply", "contact"]:
            nav = nav.replace("{a_%s}" % key, 'aria-current="page"' if key == active else "")
        head = HEAD.format(title=meta["title"], description=meta["description"], canonical=canonical,
                           site=SITE, extra_head=meta.get("extra_head", ""))
        (ROOT / f"{slug}.html").write_text(head + nav + body + FOOTER + TAIL)
        print("built", slug)


if __name__ == "__main__":
    build()
