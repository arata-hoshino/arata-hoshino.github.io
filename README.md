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

The stylesheet is a translation of the portfolio deck into continuous reading. The rules it
follows, in the order they matter:

**One typeface.** Body and headings use **Jost**, a geometric sans in the Futura tradition,
loaded from Google Fonts in `_layouts/default.html`. Jost comes ahead of the locally installed
**Futura** on purpose: macOS ships Futura in Medium and Bold only, which reads too heavy for
body copy, while Jost has a genuine Light. Code uses **IBM Plex Mono**.

**Hierarchy by size, not weight.** Body copy is 12pt at weight 400; titles are up to 2.9rem at
weight 300 — lighter than the text they head, and winning on size alone. Only `**bold**` goes
to 600. Contrast comes from scale, colour and space instead.

**Three greys and one navy.** `--ink` for titles, `--body` for running text, `--muted` for
every label and caption, and `--navy` (`#1b3a5c`) as the only colour — it marks labels, list
numbers and links, and nothing else.

**The uppercase label.** Running head, `h3`, table headers, metadata keys, the pager and the
footer are all one shape: small, uppercase, letterspaced 0.14–0.18em, muted or navy.

**Hairlines, never boxes.** Sections are separated by 1px rules and whitespace. The only
filled surfaces are code blocks, in `--tint`.

Markdown maps onto the deck's components: `h2` is a section statement announced by a rule,
`h3` is a navy column label, ordered lists become the deck's `01 / 02 / 03` rows with a
hairline between items, and figure captions sit right-aligned under the image.

**One centred column.** The running head, the rules, the text and the footer all share a
72ch column centred on the page, so every edge lines up. Lines of text stay left-aligned
inside it.

To retune the scale, edit `--body-size` and `--measure` at the top of `assets/css/style.css`
— `--frame` follows the measure, and everything else is in `em`.
