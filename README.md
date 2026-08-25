# Medbewstorstok Notes

A minimal, essay-first Jekyll site in the style of a printed series: a geometric-sans masthead, a
table of contents shared by every page, and one narrow reading column for the text.

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
| `_includes/masthead.html` | Title, subtitle and table of contents |
| `_layouts/` | `default`, `home`, `essay`, `page` |
| `assets/css/style.css` | All styling (light and dark) |

Site title, subtitle and author live in `_config.yml`.

## Local preview

```bash
bundle install
bundle exec jekyll serve --livereload
```

Then open <http://localhost:4000>. Pushing to `main` publishes via GitHub Pages.

## Fonts

Body and headings use **Futura**, falling back to **Jost** (a near-identical geometric sans
loaded from Google Fonts) on machines without Futura installed. Code uses **IBM Plex Mono**.
Both web fonts are loaded in `_layouts/default.html`. To change the typeface, edit that
`<link>` and the `--sans` / `--mono` variables at the top of `assets/css/style.css`.
