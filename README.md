# Daniel Woldetsadik — Engineering Portfolio

Buildless HTML, CSS, and JavaScript. Compatible with GitHub Pages; no package installation or build required.

## Preview

Run `python3 -m http.server 8000` from this directory and open http://localhost:8000.

## Structure

- `index.html`: introduction and two category panels.
- `hardware.html`: five filterable hardware areas.
- `software.html`: all eleven existing software projects, with filters.
- `projects/`: individually addressable project pages.
- `assets/style.css`: responsive styles, category illustrations, reduced-motion support.
- `assets/app.js`: project filtering and current copyright year.

## Add project materials

Edit the corresponding file in `projects/`. Replace a `.doc-slot` placeholder with real content, for example:

```html
<section class="doc-slot">
  <h3>AC analysis</h3>
  <img src="../assets/analog-ic/ac-response.png" alt="AC response showing …" style="max-width:100%;height:auto">
  <p>State test conditions and verified results here.</p>
  <a class="text-link" href="../assets/analog-ic/design-report.pdf">Read design report</a>
</section>
```

Create asset folders as needed. Use relative paths so links work under GitHub Pages project paths. Videos can use the standard HTML `<video controls>` element. No upload backend is provided; add files to the repository locally.

Hardware areas other than FPGA are clearly marked as awaiting documentation. No circuit metrics, device results, robotics details, or lab accomplishments have been invented. Degree wording reflects Electrical & Computer Engineering + Financial Engineering. Google Fonts are optional; local system fallbacks render without network access.

## Deployment

Nothing has been published. When ready, the contents of this directory can be served directly by GitHub Pages from the repository root.

## Technical media and interaction

Each project page contains commented, ready-to-adapt HTML for real Cadence schematic exports, Spectre plots, architecture diagrams, captioned MP4 demonstrations, and linked PDF reports. Replace a placeholder section with the relevant markup and supply actual files in `assets/<project>/`. Do not uncomment example paths until their files exist.

Use `<figure class="project-media">` for full-width media within `.doc-grid`. Wrap an image in `<a href="original.png" data-lightbox>` to enable an accessible expanded viewer with Escape-to-close, focus restoration, captions, and a full-resolution link. The original link works without JavaScript. Include descriptive image alternatives, simulation conditions in captions, video captions and a nearby text transcript. The viewer is initialized only on pages with real media links.

Homepage circuit pulses and code typing finish in under five seconds. Page navigation uses native cross-document view transitions where supported, with standard navigation elsewhere. Filters animate newly visible cards. Reduced-motion preferences disable all movement and reveal code immediately.

Major updated to Electrical & Computer Engineering + Financial Engineering. No real engineering assets were supplied or fabricated.

## PMOS navigation homepage

The abstract cross-section uses a gate over an insulating oxide and two p+ regions within an n-well. It is a navigation metaphor, not a fabrication drawing or simulation result. Gate links to Software; Drain links to Electrical & Hardware; Body scrolls to About; Source scrolls to Résumé / Contact. No résumé file was supplied, so the contact section offers an email request rather than a broken download.

On mobile, the diagram sits above a two-column grid of the same four accessible links. Hover and keyboard focus illuminate the related region. Signal flow has a pause control and respects reduced motion. All destinations work without JavaScript. The dark theme extends to collection and project pages for continuity.

## Recruiter usability update

The homepage now leads with name, education, a prominent “Request my résumé” email action, and four large plain-language navigation cards. The PMOS drawing is a static decorative reference; it is no longer necessary for navigation. All decorative animation, glows, and pulsing are disabled site-wide. The layout is wider, text is larger, and navigation/filter controls have larger hit areas. A résumé PDF has not been supplied; no download is fabricated. To offer a direct résumé later, add the real PDF and replace résumé-request links with its relative path.

## Restored centered navigation

The homepage again centers a large static PMOS diagram, surrounded by Software (top), Electrical & Hardware (right), Résumé / Contact (left), and About Me (bottom). Large plain-language labels remain primary; terminal names are secondary. On narrow screens Software appears above the diagram, Contact and Hardware sit side by side below it, and About follows. Motion and glows remain disabled. No project content was changed.

## Dimensional PMOS treatment

The centered map retains its four original destinations. Layered silicon edges, metallic gate gradients, a static soft spotlight, and restrained shadows add depth. Panels lift slightly on hover and keyboard focus. The decorative center floats by five pixels and tilts at most two degrees with a fine pointer; touch devices do not tilt. Low-contrast trace dashes travel slowly without blinking. “Pause motion” stops the floating, trace motion, parallax, and panel movement. Reduced-motion preferences automatically disable these effects, including if the preference changes while the page is open. Navigation remains standard links and needs no JavaScript. No project content or results were changed.

## Unified semiconductor core

The PMOS now uses a tighter SVG viewBox and a wide dedicated grid area, making the silicon body substantially larger. Software connects above the core; Hardware connects on its right. About and Résumé / Contact share one full-width bottom foundation section with real background text, résumé request, email, GitHub, and LinkedIn. Existing `#about` and `#contact` links still work.

Curved SVG tethers are calculated from the actual element bounds after resize and font loading. Muted traveling dash segments move outward from the core over static continuous paths; the curves remain steady for readability. This suggests guided rope/signal flow without glow or blinking. The existing Pause motion control and reduced-motion support stop the animated overlays. On mobile the branches stack in reading order, with recalculated connectors. If JavaScript is unavailable, all navigation and content remain available; decorative tethers are omitted. Project pages remain unchanged.

## Suspended panel refinement

Each branch now has two curved ropes, each drawn with a dark underside, a muted cable body, a fine static fiber pattern, and circular attachment fittings. Two attachment points visually support each panel. Panel and rope endpoints are updated from the same coordinates, so connectors remain attached during motion.

The PMOS stays fixed. Work panels drift by at most 1.35px horizontally, 0.35px vertically, and 0.10 degrees; the large About / Résumé foundation uses at most 0.65px and 0.035 degrees. Cycles last 14–15.5 seconds. No bounce, traveling signals, blinking, or glow. Hovering or focusing a panel freezes movement for targeting. Pause motion and reduced motion disable sway. Updates are capped near 30fps and stop while offscreen or the document is hidden. Layout is remeasured only on resize/font changes, not every frame.

## Suspension polish

The existing composition is retained with a wider desktop canvas, a larger central device, and balanced headline sizes for the two work branches. Cables now use restrained curves, continuous metallic highlights, and double-ring mounting eyelets instead of rope-like dash texture. Panels have a shallow visible lower edge and soft layered shadows. About / Résumé content is preserved in a more compact two-column desktop foundation. Sway is reduced to at most 0.7px and 0.045 degrees (0.3px and 0.015 degrees for the foundation); pause, hover/focus freeze, reduced-motion, and offscreen suspension remain supported.

## Separate source and body attachments

Gate continues to Software and Drain to Hardware. Body cables now attach above the About half only. A matching source cable starts at the exposed left terminal and routes around the outer left edge and beneath the shared foundation to an independent mounting point under Résumé / Contact. This perimeter route avoids crossing the Body cables or covering content. Both lower destinations share the same very small panel motion; all attachment points use the same transformation. Mobile stacking and pause/reduced-motion support are retained.

## Simplified balanced homepage

The PMOS is smaller and centered between About Me (left) and Electrical & Hardware (right), with Software above. The illustration is a static visual motif. A prominent Résumé / Contact action beside the introduction reaches the contact section below. Full About and Résumé content remains together below the hero, without suspension attachments. All rope rendering, attachment hardware, sway loops, pointer tilt, and pause controls have been removed; two short static guide lines remain for Software and Hardware. Mobile stacks Software, the motif, About, and Hardware. Standard links, focus outlines, and reduced-motion support are retained.


## Featured ESE 5620 Figure 5 amplifier

`projects/figure5-amplifier.html` documents the completed differential CMOS amplifier. It is linked from `hardware.html` and `projects/analog-ic.html`. `assets/figure5/` contains a net-labeled schematic redraw, DC transfer/gain/headroom figures in SVG and PNG, copied source CSV/netlist/validation data, reproduced metrics, and SHA-256 provenance. The original Cadence artifact folder is read-only input and was not changed.

`scripts/build_figure5.py` regenerates the figures using NumPy and Matplotlib from the original local Figure 5 artifacts. The archived local gain of −2440.91549 V/V was reproduced from the stored 20 nV PSF-ASCII sweep. The page also documents a corrected additive nodal calculation (−2473.09568 V/V), preserving the original archived theoretical value for comparison. No new simulation, layout, measurement, or AC/PVT results are claimed. Homepage HTML, animation JavaScript, and global stylesheet are unchanged.
