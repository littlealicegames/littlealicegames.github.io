# Little Alice Games website

Official portfolio website for Little Alice Games, published at
<https://littlealicegames.github.io/>.

## Structure

- `index.html` contains the page content and structured metadata.
- `styles.css` contains the complete responsive design; there is no JavaScript runtime.
- `assets/images/` contains optimized, checked-in web artwork.
- `assets/fonts/` contains self-hosted Fredoka and Atkinson Hyperlegible Next font files and their OFL licenses.
- `tools/optimize_assets.py` documents how the current web image set was produced from local studio source artwork.

## Publishing

GitHub Pages serves the `main` branch from the repository root. Pushing a commit to `main`
publishes the update automatically. The separate Croak Wars privacy-policy project remains at
<https://littlealicegames.github.io/croak-wars-privacy-policy>.

## Maintenance

Keep the contact address, product status, Google Play link, copyright year, sitemap date, and
structured data in sync whenever the public content changes. Run a Lighthouse check before
publishing material layout or asset changes.
