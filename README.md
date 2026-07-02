# The Contemporary Artist's Guide to Industrial Displays

A practical research guide for selecting, modifying, and maintaining industrial displays, touch monitors, panel PCs, Android signage displays, and related display systems for long-lived media artworks and studio installations.

The guide is written for artist-technologists who need displays that can run custom software reliably, be repaired or replaced later, and remain serviceable in museum or gallery contexts over long time spans.

## Start Here

- [The Contemporary Artist's Guide to Industrial Displays](contemporary-artists-guide-to-industrial-displays.md) is the main guide.
- [Industrial Panel PCs for Media-Art Installations](panel-pc-buying-guide.md) is the companion buying report focused on panel PC vendors, Linux compatibility, lifecycle support, and real-time graphics tradeoffs.
- [Combined PDF](contemporary-artists-guide-to-industrial-displays.pdf) bundles the research into a single shareable document.

## Updating the Guide

Edit the Markdown source files first, then rebuild the PDF:

```sh
make pdf
```

Commit both the Markdown updates and the regenerated PDF so the browser-readable and downloadable versions stay in sync.

## Evidence Labels

The guide uses explicit evidence labels such as `[datasheet]`, `[vendor page]`, `[supplier claim]`, `[teardown]`, `[forum]`, `[kernel]`, `[inferred]`, and `[unverified]`. When updating the research, preserve those labels and prefer dated, directly verifiable sources over product-listing summaries.

## Repository Contents

- `contemporary-artists-guide-to-industrial-displays.md` - main guide
- `panel-pc-buying-guide.md` - companion panel PC report
- `contemporary-artists-guide-to-industrial-displays.pdf` - combined PDF
- `Makefile` - helper command for rebuilding the PDF from the Markdown sources

## License

No public reuse license has been selected yet.
