# Medbewstorstok Notes

A minimal, essay-first Jekyll site set in the type system of the Arata Hoshino portfolio deck:
a running head over a hairline rule, large light titles, uppercase letterspaced labels, and one
navy accent. See [Design](#design).

## Writing a new essay

Create a Markdown file in `_essays/`. The filename becomes the URL
(`_essays/my-essay.md` → `/essays/my-essay/`).

```markdown
---
title: "The Title of the Essay"
number: "VI"        # shown before the title in the TOC; optional
order: 7            # controls the position in the TOC and the pager
date: 2026-08-25
summary: "One sentence shown under the title and in the index."
---

Your text, in plain Markdown. Headings, lists, tables, blockquotes,
code blocks, images and footnotes[^1] are all styled.

[^1]: Footnotes render at the bottom of the page.
```

`order` is the only field that matters mechanically — everything else is presentation.
The essay appears automatically in the top table of contents, in the index on the front
page, and in the previous/next pager at the foot of neighbouring essays.

## Structure

| Path | Purpose |
| --- | --- |
| `_essays/` | One Markdown file per essay |
| `index.md` | The introduction and the series index |
| `about.md` | About page |
| `_includes/runhead.html` | Running head and navigation |
| `_layouts/` | `default`, `home`, `essay`, `page` |
| `assets/css/style.css` | All styling |

Site title, subtitle and author live in `_config.yml`.

## Local preview

```bash
bundle install
bundle exec jekyll serve --livereload
```

Then open <http://localhost:4000>. Pushing to `main` publishes via GitHub Pages.

## Design

The layout is a translation of the portfolio deck; the type is Lora, with the body metrics
taken from situational-awareness.ai. The rules it follows, in the order they matter:

**One typeface, header included.** Body, headings and labels are all **Lora** (Cyreal, SIL
Open Font License), self-hosted as woff2 in `assets/fonts/` — see the README there. Code is
**IBM Plex Mono**, the one thing still loaded from Google Fonts.

**Two files, every weight.** Both Lora files are variable along one `wght` axis from 400 to
700, upright and italic, so 78KB covers the whole site. Body and labels are 400, `h2` is 600,
`**bold**` and `h4` are 700, and the 800 on the title and the deck resolves to 700 — the top
of the axis.

**The text settings**, after [situational-awareness.ai](https://situational-awareness.ai/) —
that page measures 18px, line-height 1.5, a 740px column, ~95 characters a line. This site
takes it a step down: **17px, line-height 1.5, a 700px column**, ~80 characters a line. Titles
run to 2.95rem and `h2` to 1.45em.

**Three greys and one navy.** `--ink` for titles, `--body` for running text, `--muted` for
every label and caption, and `--navy` (`#1b3a5c`) as the only colour — labels, list numbers,
links and the section rail's current marker.

**The uppercase label.** Running head, `h3`, table headers, metadata keys, the pager and the
footer are one shape: small, uppercase, muted or navy.

**No letterspacing, no rendering overrides.** Nothing on the site sets `letter-spacing`,
`font-feature-settings` or `text-rendering`. Every line is set at the metrics the face itself
specifies.

**Hairlines, never boxes.** Sections are separated by 1px rules and whitespace. The only
filled surfaces are code blocks, in `--tint`.

**One centred column, a wider frame.** The text sits in a 700px column centred on the page; the
running head, nav and footer span the wider `--frame`.

**The section rail.** `assets/js/section-rail.js` reads the `h2`/`h3` headings out of `.prose`
and builds a list of them in the left margin — click to jump, and the section you are reading
is marked as you scroll. It appears only above 78rem, where there is a margin to put it in, and
only when a page has two or more headings. The links use the ids kramdown already generates
(`auto_ids`), so nothing needs to be written by hand.

Markdown maps onto the deck's components: `h2` is a section statement announced by a rule,
`h3` is a navy column label, ordered lists become the deck's `01 / 02 / 03` rows with a
hairline between items, and figure captions sit right-aligned under the image.

To retune the scale, edit `--body-size` and `--measure` at the top of `assets/css/style.css`
— everything else is in `em` and follows.
