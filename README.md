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

Body and headings use **Jost**, a geometric sans in the Futura tradition, loaded from Google
Fonts in `_layouts/default.html`. Jost comes ahead of the locally installed **Futura** in the
stack on purpose: macOS ships Futura in Medium and Bold only, which reads too heavy for body
copy, while Jost has a genuine Light. Code uses **IBM Plex Mono**.

Body copy is 12pt at weight 300. To retune it, edit `--body-size` (and `--sans` / `--mono`)
at the top of `assets/css/style.css` — the rest of the type scale is in `em`, so it follows.
