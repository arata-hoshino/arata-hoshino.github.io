---
layout: page
title: About
permalink: /about/
description: "Who writes this, and how it is put together."
---

I am **Arata Hoshino**. I write about software systems, the tradeoffs behind them, and the
gap between architecture as drawn and architecture as run.

## How this site works

Every essay is a Markdown file in the `_essays/` directory. Jekyll reads the front matter at
the top of each file, sorts the essays by their `order` field, and builds both the table of
contents at the top of every page and the index on the front page.

To publish a new essay:

1. Create `_essays/my-new-essay.md`.
2. Give it front matter — `title`, `number`, `order`, `summary`, and `date`.
3. Write the body in Markdown.
4. Commit and push. GitHub Pages builds the rest.

To preview locally:

```bash
bundle install
bundle exec jekyll serve --livereload
```

## Elsewhere

- [GitHub](https://github.com/arata-hoshino)
