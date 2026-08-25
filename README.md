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

The layout is a translation of the portfolio deck; the typography follows the OpenAI article
pages. The rules it follows, in the order they matter:

**One typeface, header included.** Body, headings and labels are all **Inter**, a neutral
grotesque, loaded from Google Fonts in `_layouts/default.html`. OpenAI Sans, which the pages
this is modelled on use, is proprietary and undistributable, so Inter stands in for it, with
the platform grotesques (SF, Segoe, Helvetica) behind it. Code is **IBM Plex Mono**.

**The text settings.** 18px body at weight 400, line-height 1.6, no added tracking. Titles run
to 3rem, also at weight 400, with line-height 1.12 and −0.022em tracking — large and calm
rather than heavy. `h2` is 1.45em at 500. Only `**bold**` goes to 800.

**Three greys and one navy.** `--ink` for titles, `--body` for running text, `--muted` for
every label and caption, and `--navy` (`#1b3a5c`) as the only colour — labels, list numbers,
links and the section rail's current marker.

**The uppercase label.** Running head, `h3`, table headers, metadata keys, the pager and the
footer are one shape: small, uppercase, letterspaced 0.08–0.09em, muted or navy.

**Hairlines, never boxes.** Sections are separated by 1px rules and whitespace. The only
filled surfaces are code blocks, in `--tint`.

**One centred column, a wider frame.** The text sits in a 64ch column centred on the page; the
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
