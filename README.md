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

The layout is a translation of the portfolio deck; the type is Latin Modern, with the body
metrics taken from situational-awareness.ai. The rules it follows, in the order they matter:

**One typeface, header included.** Body, headings and labels are all **Latin Modern Roman**,
the Computer Modern of a LaTeX page. It is self-hosted: the OTFs come from CTAN, converted to
woff2, in `assets/fonts/` under the GUST Font License (a copy sits beside them). Latin Modern
ships Regular and Bold and nothing in between, so the type uses only 400 and 700. Code is
**IBM Plex Mono**, the one thing still loaded from Google Fonts.

**The text settings**, measured off [situational-awareness.ai](https://situational-awareness.ai/):
18px body, line-height 1.5, no added tracking, in a 740px column. That page runs about 95
characters to the line; Latin Modern is a little wider than the face it uses, so the same 740px
gives about 88. Titles run to 2.95rem at weight 400 with line-height 1.15 — large and calm
rather than heavy. `h2` is 1.45em at 700, and `**bold**` is 700.

**Three greys and one navy.** `--ink` for titles, `--body` for running text, `--muted` for
every label and caption, and `--navy` (`#1b3a5c`) as the only colour — labels, list numbers,
links and the section rail's current marker.

**The uppercase label.** Running head, `h3`, table headers, metadata keys, the pager and the
footer are one shape: small, uppercase, letterspaced 0.08–0.09em, muted or navy.

**Hairlines, never boxes.** Sections are separated by 1px rules and whitespace. The only
filled surfaces are code blocks, in `--tint`.

**One centred column, a wider frame.** The text sits in a 740px column centred on the page; the
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
