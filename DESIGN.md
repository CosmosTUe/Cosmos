---
name: Cosmos
description: Website of Cosmos, the international student association at TU/e
colors:
  blue-1: "#fafdff"
  blue-2: "#f3f8fc"
  blue-3: "#e7f1f8"
  blue-4: "#d9e9f3"
  blue-5: "#c8deed"
  blue-6: "#b1cfe3"
  blue-7: "#8fb8d3"
  blue-8: "#5f97bb"
  blue-9: "#005274"
  blue-10: "#0e6e9e"
  blue-11: "#135f85"
  blue-12: "#0f2c3b"
  text: "#454545"
  text-muted: "#5b6770"
  surface: "#ffffff"
typography:
  page-title:
    fontFamily: "Raleway, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 800
    lineHeight: 1.2
  page-title-phone:
    fontFamily: "Raleway, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 800
    lineHeight: 1.2
  card-title:
    fontFamily: "Raleway, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 800
    lineHeight: 1.2
  section-heading:
    fontFamily: "Raleway, sans-serif"
    fontSize: "1rem"
    fontWeight: 700
    lineHeight: 1.2
  lead:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  card-text:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "0.975rem"
    fontWeight: 400
    lineHeight: 1.6
  link-label:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 600
rounded:
  card: "0.75rem"
spacing:
  card-padding: "1.25rem"
  grid-gap: "1.5rem"
  header-gap: "2.25rem"
  section-gap: "2.25rem"
  page-top: "2.5rem"
  page-bottom: "3rem"
components:
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-padding}"
  card-media:
    backgroundColor: "{colors.blue-2}"
  card-media-hover:
    backgroundColor: "{colors.blue-3}"
  card-title:
    textColor: "{colors.blue-12}"
    typography: "{typography.card-title}"
  link-more:
    textColor: "{colors.blue-11}"
    typography: "{typography.link-label}"
  link-more-hover:
    textColor: "{colors.blue-10}"
  page-title:
    textColor: "{colors.blue-12}"
    typography: "{typography.page-title}"
  page-lead:
    textColor: "{colors.text-muted}"
    typography: "{typography.lead}"
  navbar:
    backgroundColor: "{colors.blue-9}"
    textColor: "{colors.surface}"
    height: "6rem"
  button-primary:
    backgroundColor: "{colors.blue-9}"
    textColor: "{colors.surface}"
  button-primary-hover:
    backgroundColor: "{colors.blue-10}"
---

# Design System: Cosmos

This guide describes where the site is going, taken from the committee pages (`/committees/` and `/committees/<slug>/`), which are the reference. Most other pages still use the older look; each one moves over in its own PR. When this guide and an old page disagree, the guide wins.

## Overview

**Creative North Star: "The Notice Board"**

The site works like a well-kept association notice board: everything has its own card, cards are easy to scan, and a visitor finds their committee, event or document without reading the whole page. It is friendly and orderly rather than flashy. Cosmos blue does the branding; the layout stays calm and predictable so the content (committees, events, photos, people) carries the personality.

Density is moderate: generous space around each card, compact text inside it. Pages lead with a plain heading and one sentence of context, then go straight into the content. Decoration is limited to the blue scale and one soft fade under the navbar on detail pages.

**Key Characteristics:**
- One brand colour, Cosmos blue, used as a 12-step scale for every tint, border and text shade.
- Raleway (extra bold) for headings, Open Sans for everything else.
- Flat cards with a thin pale-blue border; depth only appears on hover.
- The whole card is the link; navigation is text links, buttons are for actions.
- Left-aligned page headers with an intro line, not centred titles.

## Colors

A single cool blue family over white, with warm-grey body text.

### Primary
- **Cosmos Blue** (blue-9): the brand colour. The navbar, primary buttons and focus rings. Solid fills only; never as body text on white below 18px bold.
- **Bright Cosmos Blue** (blue-10): hover state of anything in Cosmos Blue, and the hover colour of text links.
- **Link Blue** (blue-11): text links and "More about…" links. Replaces Bootstrap's `#0d6efd` everywhere.
- **Ink Blue** (blue-12): page titles and card titles. Near-black with a blue cast, so headings read as Cosmos rather than generic black.

### Neutral
- **Paper** (surface): page and card background.
- **Mist** (blue-1, blue-2): the quietest tints. Image panels behind committee art (blue-2).
- **Pale Wash** (blue-3): hover fill of image panels; the start colour of the navbar fade.
- **Hairline Blue** (blue-4): card borders at rest.
- **Selection Blue** (blue-5): text selection background.
- **Soft Rule** (blue-6): dividers and input borders.
- **Hover Border** (blue-7): card border on hover; the large initial on committees without a photo.
- **Muted Steel** (blue-8): reserved for secondary icons and disabled states.
- **Body Grey** (text): running text.
- **Slate** (text-muted): intro lines, descriptions and secondary text.

### Named Rules
**The One Blue Rule.** Every colour on a page comes from the blue scale or the two greys. No other hues, and no raw hex values in templates or page CSS; use the `--cosmos-blue-*` variables.

**The Step Rule.** Steps 1–2 are backgrounds, 3–5 fills, 6–8 borders, 9–10 solid colour, 11–12 text. If a colour is doing a job outside its step range, pick another step.

## Typography

**Display Font:** Raleway (with sans-serif fallback)
**Body Font:** Open Sans (with sans-serif fallback)

**Character:** Raleway at 800 gives headings a confident, slightly geometric voice; Open Sans keeps long text neutral and readable. Both must be loaded from Google Fonts: Raleway 700 and 800, Open Sans 400 and 600. Poppins and Roboto are loaded today but unused, and should go.

### Hierarchy
- **Page title** (800, 2.25rem, 1.2; 1.875rem on phones): one per page, in Ink Blue, `text-wrap: balance`.
- **Lead** (400, 1.125rem, 1.6): the single intro sentence under the page title, in Slate, at most 40rem wide.
- **Card title** (800, 1.25rem, 1.2): the name on each card, in Ink Blue.
- **Section heading** (700, 1rem): small headings inside a detail card ("Members", "Contact"), in Cosmos Blue, with 2.25rem above and 0.25rem below.
- **Body** (400, 1rem, 1.6–1.7): running text, at most about 70 characters per line.
- **Card text** (400, 0.975rem, 1.6): descriptions inside cards, in Slate, `text-wrap: pretty`.
- **Link label** (600, 0.95rem): "More about…" style links, in Link Blue.

### Named Rules
**The Real Heading Rule.** Use heading levels for structure, not size: one `h1` per page, `h2` for cards or sections. Size comes from the role above, never from picking `h5` because it looks right.

**The No Global Paragraph Rule.** Paragraphs are 1rem with no top margin. The old site-wide rule (`p { margin-top: 2em; font-size: 18px }`) is legacy; new components must not depend on it and it will be removed.

## Layout

Pages sit in Bootstrap's container (1320px max at xxl) on Bootstrap 5.0 breakpoints (576, 768, 992, 1200, 1400px). A page has 2.5rem of space above the header and 3rem below the content (1.75rem / 2.5rem on phones). The header is left-aligned, followed by 2.25rem of space before the content.

Card grids use one column on phones and tablets and two from 992px (`row-cols-1 row-cols-lg-2`), with a 1.5rem gap. Lists that need more density may go to three columns at 1200px, never four. Inside a card, image and text sit side by side (2:3 split; a fixed 6.5rem image column on phones), so cards stay horizontal at every width.

The fixed navbar takes 6rem at the top. Detail pages may extend a full-width fade from Pale Wash to white (over 26rem) up under the navbar; it covers the full width, never a boxed area.

## Elevation & Depth

Flat by default. Surfaces are separated by thin blue borders and the tint of the image panel, not by shadows. A soft shadow appears only as feedback on hover.

### Shadow Vocabulary
- **Hover lift** (`box-shadow: 0 6px 18px -8px rgba(15, 44, 59, 0.25)`): cards on hover, together with the border moving from Hairline to Hover Border. Nothing moves or scales.

### Named Rules
**The Flat-At-Rest Rule.** Nothing has a shadow until the pointer is on it. The older always-on card shadow (`0 10px 25px rgba(0,0,0,.06)`) and the lift-on-hover (`translateY(-4px)`) are legacy.

## Shapes

Gently rounded rectangles. Cards use 12px corners (0.75rem) and clip their images to them. Images inside cards are square (1:1, `object-fit: cover`); committee art is being redrawn as squares to match. Committees without a photo show their initial, large, in Hover Border blue on the Mist panel, instead of a placeholder image.

## Components

### Cards
The core of the site: one card per committee, event, album or document.
- **Corner Style:** 12px (0.75rem), image clipped.
- **Background:** Paper; the image panel in Mist (blue-2), Pale Wash on hover; a 1px Pale Wash divider between image and text.
- **Border:** 1px Hairline Blue at rest, Hover Border on hover.
- **Shadow Strategy:** Hover lift only (see Elevation).
- **Internal Padding:** 1.25rem (1rem on phones).
- **Behaviour:** The title is the only real link and stretches over the whole card, so the whole card is clickable. The keyboard focus ring (2px Cosmos Blue, 2px offset) goes around the card, not the title. Transitions are 0.2s and switch off under `prefers-reduced-motion`.

### Links
- **Text links:** Link Blue, no underline, Bright Cosmos Blue on hover.
- **"More about…" link:** at the bottom of a card, Link Label type, followed by a chevron that moves 3px right on card hover. It repeats the card's link visually and is hidden from screen readers, since the title already is the link.

### Buttons
- **Use:** for actions only (submit, save, register, delete). Moving to another page is a link or a card, not a button. The "see more" buttons on old pages go.
- **Primary:** Cosmos Blue background, white text; Bright Cosmos Blue on hover.
- **Shape:** not settled yet. The old pages use Bootstrap's default and the committee detail page a pill; the global-fixes PR picks one.

### Page header
- Page title, then one lead sentence in Slate. No centred `h2` with `w-75 mx-auto`, no all-caps section titles.

### Navigation
- Fixed bar in Cosmos Blue, white logo on the left, white links; the current page in bold and not clickable. Collapses to a menu button below 768px.

### Detail page
- A single wide card (image left, text right on 768px and up), under the full-width navbar fade. Title in Cosmos Blue, description as body text, then optional sections with Section headings.

## Do's and Don'ts

### Do:
- **Do** take every colour from `--cosmos-blue-1` to `--cosmos-blue-12`, `--black` (body text; the global-fixes PR renames it `--cosmos-text`) or `--cosmos-text-muted`.
- **Do** make the whole card the click target with one stretched title link.
- **Do** give every list an empty state written as a plain sentence ("No committees to show yet.").
- **Do** use square images in cards, and the initial fallback when there's no image.
- **Do** check new pages at 390px, 768px and 1280px wide.

### Don't:
- **Don't** use Bootstrap's default blue (`#0d6efd`), `--light-blue` or `#124265`; they're replaced by the scale.
- **Don't** add shadows at rest, translate cards on hover, or add gradients other than the navbar fade on detail pages.
- **Don't** use "see more" buttons for navigation.
- **Don't** centre page titles or set section titles in all caps.
- **Don't** add new fonts or font weights beyond Raleway 700/800 and Open Sans 400/600.
