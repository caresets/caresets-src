# Security headers for the RIZIV/INAMI host

The site is static. Everything it needs is served from its own origin: there are
no third-party scripts, stylesheets, fonts or images, and no external network
call at runtime. That is enforced in the page itself by a
`Content-Security-Policy` in `<meta>`, set in `_includes/head_custom.html`.

`DELIVERY-NOTE.md` describes the same package for a non-technical reader. The
two documents are meant to agree; if they ever diverge, the built package
decides.

A `<meta>` policy cannot express everything. The headers below have to come from
the web server or CDN in front of the site, and are what remains to be set at
the hosting layer.

## Required

| Header | Value | Why |
|---|---|---|
| `Content-Security-Policy` | see below | A real header supersedes the `<meta>` one and covers the theme's stylesheet and `just-the-docs.js`, which are parsed before the meta tag applies. |
| `X-Frame-Options` | `DENY` | `frame-ancestors` is **ignored** in a `<meta>` policy, so clickjacking is currently unmitigated. Either this header or `frame-ancestors 'none'` in the CSP header below. |
| `X-Content-Type-Options` | `nosniff` | Stops a browser from re-interpreting a `.json` or `.csv` response as HTML or script. |
| `Referrer-Policy` | `same-origin` | Glossary URLs carry concept codes in the path and fragment. Do not send them to external sites the user clicks through to. |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Only once HTTPS is confirmed working on the final hostname. |

The CSP as a header, matching what the pages already declare, plus the two
directives `<meta>` cannot carry:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
```

## Recommended

| Header | Value | Why |
|---|---|---|
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=(), payment=(), usb=()` | The site uses none of these; deny them outright. |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolates the browsing context. |
| `Cross-Origin-Resource-Policy` | `same-origin` | Stops other sites embedding the generated CodeSystem JSON directly. |

## Scripts: `'unsafe-inline'` is not used

`script-src` is `'self'` with **no** `'unsafe-inline'`. Every executable script
is a file under `assets/js/`, so script injected into a page does not run —
which is the directive that mitigates XSS, as against merely blocking foreign
origins.

The twelve inline blocks the site used to carry were moved into files. Page
values reach them through `<script type="application/json">` elements, which
are data rather than code and so are not subject to `script-src`.

Supporting measures, in case a reviewer asks how the data itself is handled:
the pages render content from generated files in this repository, not from user
input; the one attacker-controllable input — the `?model=` parameter on the
model viewer — is validated against `^[A-Za-z0-9._-]{1,128}$` and HTML-escaped
everywhere it reaches the DOM; and there is no `eval`, `new Function`,
`document.write` or `insertAdjacentHTML` anywhere in the site's own JavaScript.

## Remaining gap: `style-src`

`style-src` still allows `'unsafe-inline'`. The just-the-docs theme emits inline
`<style>`, and the layouts use `style="..."` attributes throughout, which CSP
also governs. Injected CSS is a substantially smaller problem than injected
script; closing this would mean rewriting the site's styling into stylesheets.

A `<meta>` policy also cannot express `frame-ancestors` or `report-uri`, which
is why the header above is still needed from the hosting side.

## Third-party code, as vendored

No CDN is used. The scripts live in `assets/js/vendor/` and the fonts in
`assets/fonts/`, each pinned by filename, with the scripts' SHA-256 recorded in
`_includes/head_custom.html`. Nothing updates automatically — a published
vulnerability in any of them is a manual upgrade here.

| Library | Version | Licence | Used for |
|---|---|---|---|
| jQuery | 3.7.0 | MIT | required by DataTables |
| DataTables | 1.13.6 | MIT | search, sort and paging on the glossary and model tables |
| DataTables Buttons | 2.4.2 | MIT | the CSV download button |
| DataTables Buttons HTML5 | 2.4.2 | MIT | generates the CSV in the browser |
| Noto Sans (16 files) | — | SIL OFL 1.1 | typography, self-hosted |
| just-the-docs | 0.12.0 | MIT | page layout and navigation |
| lunr.js | — | MIT | ships with the theme; unused, site search is disabled |

Excel and PDF export are switched off in `_config.yml` under `exports:`, so
**JSZip and pdfMake are not in the package** — roughly 2.25 MB of third-party
document-generation code that no page loads. Turning either format back on
means re-enabling its flag *and* removing the matching line from the Jekyll
`exclude:` list; the two are commented as a pair. CSV download needs no extra
library and is retained.
