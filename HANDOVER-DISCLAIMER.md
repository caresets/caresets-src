# Handover statement and disclaimer

**Package:** `riziv-inami-site.zip`
**SHA-256:** `cbbe9a03c7ea6a97aa9d3073095d987a33a357d0843b4286688e40efd987e402`
**Contents:** 143 files, 6.3 MB unpacked
**Built from:** commit `d1f3339`, Jekyll 4.4.1 on Ruby 3.4.9
**Date:** 30 August 2026

Everything stated below applies to **this package only**, identified by the
hash above. If the package is rebuilt, modified, or any file in it is changed
after delivery, these statements no longer describe what is being deployed.

To confirm you are holding the file these statements describe:

```
Windows   certutil -hashfile riziv-inami-site.zip SHA256
Linux/mac sha256sum riziv-inami-site.zip
```

Note that rebuilding the site from source produces a **different** hash even
when the content is identical, because a zip archive records the time each
file was added. Verify against the file you were given; do not rebuild and
compare.

> This is a technical handover statement, not legal advice. Where a contract
> or framework agreement between the parties sets out liability, warranty or
> acceptance terms, those terms govern and this document does not vary them.

---

## 1. What is being delivered

A static website: HTML, CSS, JavaScript, JSON, fonts and images. It contains no
server-side code, no database, no installer and no runtime dependency. The web
server is only required to return the files as they are.

It is content and presentation for the CareSets glossary and logical models. It
is not an application, and it neither authenticates users nor processes input.

## 2. What has been checked, and how

The following were verified by **inspecting the built package** — the same
artefact identified by the hash above — rather than assumed from the source:

- no cookies are set, and no `localStorage` or `sessionStorage` is written
- no analytics, tag manager or telemetry of any kind is present
- every script, stylesheet, font and image is served from the package itself;
  no request is made to any third-party domain
- the single `<form>` has no `action` and submits nothing
- a `Content-Security-Policy` of `default-src 'self'` is present on all 48
  HTML pages, with `script-src 'self'` and no `'unsafe-inline'`
- no executable inline `<script>` remains; page data travels as
  `<script type="application/json">`
- no `eval`, `new Function`, `document.write` or `insertAdjacentHTML` appears
  in the site's own JavaScript
- the one URL parameter the site reads is validated against
  `^[A-Za-z0-9._-]{1,128}$` and HTML-escaped before display
- no credentials, API keys or internal working documents are included
- no draft or unapproved terminology is included

`DELIVERY-NOTE.md`, included with the package, records these in more detail and
sets out four checks a reviewer can repeat independently.

## 3. What has **not** been done

This list is deliberate. Absence of a check is not a finding of safety.

- **No penetration test or formal security assessment.** The statements in
  section 2 come from inspection, not from adversarial testing.
- **No third-party code review.** The libraries listed in section 4 are used as
  published by their authors. Their source has not been read or audited.
- **No accessibility (WCAG) audit**, and no assessment against any Belgian or
  EU accessibility obligation that may apply to a public-sector site.
- **No cross-browser or assistive-technology testing matrix.** The site has
  been exercised in ordinary desktop browsing only.
- **No load, performance or availability testing.**
- **No GDPR/AVG assessment of the published content.** The site collects no
  personal data; whether the terminology it displays is appropriate for
  publication is a matter for the content owner.
- **No verification of the hosting environment**, its configuration, TLS,
  access control, logging or backup.

## 4. Third-party components

Included and unmodified, each under a permissive open-source licence:

| Component | Version | Licence |
|---|---|---|
| jQuery | 3.7.0 | MIT |
| DataTables | 1.13.6 | MIT |
| DataTables Buttons | 2.4.2 | MIT |
| DataTables Buttons HTML5 | 2.4.2 | MIT |
| just-the-docs (theme) | 0.12.0 | MIT |
| lunr.js (ships with the theme, unused) | — | MIT |
| Noto Sans (16 font files) | — | SIL Open Font License 1.1 |

These are pinned by version and **do not update themselves**. A vulnerability
published against any of them after the date above will not be fixed by
anything in this package; it requires a new build. The versions are listed so
they can be checked against advisories.

## 5. What the deploying team remains responsible for

Delivery of this package does not transfer these:

- **HTTP response headers.** The package cannot set them. `X-Frame-Options` or
  `frame-ancestors` in particular **cannot** be enforced from inside the
  package, so clickjacking protection depends entirely on the server. The
  requested headers are in `SECURITY-HEADERS.md`.
- **TLS configuration and certificate management.**
- **Access control**, if the site is not intended to be fully public.
- **Logging, monitoring, backup and restore.**
- **Applying future updates**, including for the third-party components above.
- **Confirming the deployment is fit for its purpose** in the target
  environment, including any organisational security review, accessibility
  obligation or publication approval that applies.

## 6. Scope of this statement

The statements in section 2 describe the package as delivered on the date
above. They are provided in good faith, on the basis of the checks described,
and without warranty that the package is free of defects or fit for any
particular purpose.

Any modification to the package after delivery — including rebuilding it,
editing files, or deploying it alongside other content on the same origin —
invalidates them, because they were verified against this artefact and no
other.

Questions about anything in this document should be raised **before**
deployment rather than after.
