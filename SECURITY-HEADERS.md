# Security headers for the RIZIV/INAMI host

The site is static. Everything it needs is served from its own origin: there are
no third-party scripts, stylesheets, fonts or images, and no external network
call at runtime. That is enforced in the page itself by a
`Content-Security-Policy` in `<meta>`, set in `_includes/head_custom.html`.

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
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
```

## Recommended

| Header | Value | Why |
|---|---|---|
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=(), payment=(), usb=()` | The site uses none of these; deny them outright. |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolates the browsing context. |
| `Cross-Origin-Resource-Policy` | `same-origin` | Stops other sites embedding the generated CodeSystem JSON directly. |

## Known gap: `'unsafe-inline'`

`script-src` still allows inline script because twelve layouts and includes carry
inline `<script>` blocks, several of which interpolate Liquid variables — so
their content differs per page and CSP hashes cannot be used. The policy
therefore blocks **foreign origins**, not injected inline script.

What limits the exposure in practice: the pages render data from generated files
in this repository, not from user input, and the one attacker-controllable input
— the `?model=` parameter on the model viewer — is validated against
`^[A-Za-z0-9._-]{1,128}$` and HTML-escaped everywhere it reaches the DOM
(`assets/js/model-viewer.js`). There is no `eval`, `new Function`,
`document.write` or `insertAdjacentHTML` anywhere in the site's own JavaScript.

Closing the gap properly means moving those inline blocks into files under
`assets/js/` and passing page variables through `data-` attributes, after which
`'unsafe-inline'` can be dropped from `script-src`.

## Third-party code, as vendored

No CDN is used. These are committed under `assets/js/vendor/`, pinned by
filename, with their SHA-256 recorded in `_includes/head_custom.html`. Nothing
updates them automatically — a published vulnerability in any of them is a
manual upgrade here.

| Library | Version | Used for |
|---|---|---|
| jQuery | 3.7.0 | required by DataTables |
| DataTables | 1.13.6 | the glossary and model tables |
| DataTables Buttons | 2.4.2 | the export and print buttons |
| JSZip | 3.10.1 | Excel export only |
| pdfmake + vfs_fonts | 0.2.7 | PDF export only |

JSZip and pdfmake together are roughly 2.25 MB and are loaded on every page,
including pages with no table. They exist solely for the Excel and PDF export
buttons. If those are not required, removing them is the single largest
reduction in third-party code available.
