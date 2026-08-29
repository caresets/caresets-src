# CareSets glossary — delivery note

**Package:** `riziv-inami-site.zip`
**Contents:** a static website — 147 files, 6.5 MB
**Prepared:** 29 August 2026

This note describes exactly what is in the package, what it does, and what the
hosting environment still needs to provide. It is written so that it can be
handed to whoever reviews minisites, without them needing to read the code.

---

## 1. What this is

A **static website**. Unzip it into a web root and it works. There is:

- **no server-side code** — no PHP, no .NET, no Node, no CGI
- **no database**
- **no build step or runtime dependency** on the hosting side
- **no login, no user accounts, no admin interface**

Every file is HTML, CSS, JavaScript, JSON, a font, or an image. The web server
only ever has to return files as-is.

## 2. What it does not do

Each of these was verified against the built package, not assumed:

| | |
|---|---|
| Sets cookies | **No** — no cookie is written anywhere |
| Stores data in the browser | **No** — no localStorage or sessionStorage is written |
| Analytics or tracking | **No** — no Google Analytics, no tag manager, no beacons |
| Calls any external server | **No** — every request the pages make is to their own origin |
| Loads anything from a CDN | **No** — all scripts, styles and fonts are inside the package |
| Submits data anywhere | **No** — the one `<form>` is a download selector handled entirely in the browser; it has no `action` and posts nothing |
| Collects personal data | **No** — the site displays terminology only |

Because nothing is loaded from a third-party domain, **no visitor's IP address
is disclosed to any external party**, including font and script providers. This
was a deliberate change: Google Fonts and four CDNs were removed and their
content brought inside the package.

## 3. Security measures already built in

- **Content-Security-Policy** on all 48 pages, `default-src 'self'`. The browser
  will refuse to load any script, style, font, image or network request from
  another origin, even if one were somehow injected.
- **No inline JavaScript.** `script-src 'self'` with no `'unsafe-inline'`: every
  script is a file in the package, so injected script does not execute. Page
  data is passed as `<script type="application/json">`, which is data.
- **`object-src 'none'`** — no Flash/Java/plugin embedding.
- **`base-uri 'self'`, `form-action 'self'`** — a page cannot be made to
  re-target its links or submissions.
- All text drawn from data files is HTML-escaped before display, and the single
  URL parameter the site accepts (`?model=`) is validated against
  `^[A-Za-z0-9._-]{1,128}$` before use.

## 4. Third-party components included

All are widely used, MIT-licensed, and present as their official published
files. Nothing is modified.

| Component | Version | Licence | Why it is there |
|---|---|---|---|
| jQuery | 3.7.0 | MIT (OpenJS Foundation) | required by DataTables |
| DataTables | 1.13.6 | MIT (SpryMedia) | search, sort and paging on the glossary tables |
| DataTables Buttons | 2.4.2 | MIT (SpryMedia) | the CSV download button |
| DataTables Buttons HTML5 | 2.4.2 | MIT (SpryMedia) | generates the CSV in the browser |
| Noto Sans (16 font files) | — | SIL Open Font License 1.1 | page typography, self-hosted |
| just-the-docs theme | 0.12.0 | MIT | page layout and navigation |
| lunr.js | — | MIT | ships with the theme; **unused**, site search is disabled |

Excel and PDF export were **switched off** and their libraries (pdfMake, JSZip —
2.1 MB) are **not in the package**. They can be re-enabled, but that means
adding third-party code that parses and generates documents in the visitor's
browser. CSV download is retained and needs no extra library.

## 5. What the hosting environment must provide

The package cannot set HTTP headers — only the web server can. These are
requested:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

The first two matter most: `frame-ancestors` / `X-Frame-Options` prevent the
site being framed by another page, and that **cannot** be done from inside the
package. Everything else is already enforced by the page itself.

See `SECURITY-HEADERS.md` for the reasoning behind each.

## 6. Stated honestly: known limitations

- **`style-src` still allows inline styles.** The page layout uses inline
  `style="..."` attributes throughout. Injected CSS is a much smaller problem
  than injected script, which is blocked; removing this would mean rewriting the
  site's styling.
- **Third-party libraries are pinned and will not auto-update.** A future
  vulnerability in jQuery or DataTables requires a new package. The versions are
  listed above so they can be checked against advisories.
- **The site has not been penetration-tested.** The statements above come from
  inspecting the built package.
- **Four models marked `draft` are included** under `_resources/models/draft/`.
  They are reachable by direct URL though not linked in navigation. If draft
  material should not be published, say so and they will be removed.

## 7. Where the content comes from

The glossary terms and definitions are generated from a maintained Excel
workbook; the logical models are the FHIR StructureDefinitions exported from the
eHealth Core Clinical package (export of 29 August 2026). Both are converted to
the published files by scripts kept with the source, so the site can be
regenerated and the output is reproducible.

The definitions were reviewed in August 2026 against ISO 704:2022 and
ISO/IEC Directives Part 2 for terminological quality; 83 findings were recorded
and individually approved or rejected.

## 8. How a reviewer can verify this themselves

Without reading any code, on the unzipped package:

- **No external calls:** search all files for `http://` and `https://` — every
  hit is a hyperlink for the reader to click, an XML namespace, or a
  documentation reference. None is a script, stylesheet, font or image source.
- **No inline script:** search the HTML for `<script>`. Every script tag either
  has a `src=` pointing inside the package, or is `type="application/json"`
  (data, which browsers do not execute).
- **The policy is present:** search for `Content-Security-Policy`; it appears in
  all 48 HTML pages.
- **Open it offline:** the site renders from the local filesystem with no
  network connection, which demonstrates it needs nothing external.
