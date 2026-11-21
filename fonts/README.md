# Bundled Noto fonts

The report and Python charts load these local files directly. No Windows font installation is required.

- Hebrew body: Noto Sans Hebrew, width 100, weights 400 and 700.
- Hebrew headings: Noto Sans Hebrew Condensed, width 75, weight 700.
- English: Noto Sans, width 100, weights 400 and 700; true italic faces are included.
- A matching condensed English bold instance is available for future headings.

The static TTF instances were prepared from the Google Fonts variable files on 2026-11-21 using `fontTools.varLib.instancer` 4.68.0, pinning both `wght` and `wdth` and updating the instance names. There is no outline slant or horizontal scaling in the template.

Upstream files:

- [Noto Sans Hebrew](https://github.com/google/fonts/tree/main/ofl/notosanshebrew)
- [Noto Sans](https://github.com/google/fonts/tree/main/ofl/notosans)

Each family retains its own SIL OFL 1.1 license in this folder. `font-manifest.json` records the axis settings and SHA-256 hashes of both the downloaded variable source and each prepared instance. The variable sources are not duplicated in this repository.
