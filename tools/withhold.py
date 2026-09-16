#!/usr/bin/env python3
"""
Hold a chapter back at its opening, the same amount in every chapter.

    python3 tools/withhold.py _essays/on-building.md ...

The chapters open at very different lengths, so cutting at the first
numbered section gave a page of two hundred words in one chapter and
eleven hundred in another. This cuts to a word count instead, so the fade
at the foot of the page begins at the same place in all of them. A
paragraph that runs past the count is cut at a sentence, which is what
the fade is covering anyway.

What is not published is not served either: nothing below the cut reaches
the page. The notes the retained text cites are kept, and they are always
the leading run, so their numbering still matches the marks in the text.

Run it after tools/import_chapter.py.
"""

import io
import re
import sys

LEAD = 240                      # words of each chapter that stay published

NOTE = re.compile(r'^(\d+)\. .*?(?:\n\{: #note-\1 \.note\})', re.M | re.S)
SENTENCE = re.compile(r'(?<=[.!?])\s+')


def lead(body):
    """The opening of a chapter, cut to LEAD words."""
    heads = list(re.finditer(r'^## .+$', body, re.M))
    seg = body[:heads[1].start()] if len(heads) > 1 else body

    out, n = [], 0
    for block in (b for b in seg.split('\n\n') if b.strip()):
        # plates are left out: one of them is worth a screen of prose, and
        # the page would no longer be the same length as its neighbours.
        # An epigraph is not a plate and stays where it was written.
        if 'class="epigraph"' in block:
            out.append(block)
            continue
        if block.lstrip().startswith(('<figure', '<div')):
            continue
        if block.lstrip().startswith('#'):
            out.append(block)
            continue

        words = len(block.split())
        if n + words <= LEAD:
            out.append(block)
            n += words
            continue

        # the paragraph that crosses the count is cut at a sentence
        kept = []
        for sentence in SENTENCE.split(block):
            if n >= LEAD:
                break
            kept.append(sentence)
            n += len(sentence.split())
        if kept:
            out.append(' '.join(kept))
        break

    while out and out[-1].lstrip().startswith('#'):
        out.pop()
    return '\n\n'.join(out), n


def withhold(path):
    text = io.open(path, encoding='utf-8').read()
    _, head, rest = text.split('---\n', 2)
    body, _, apparatus = rest.partition('<div class="apparatus"')

    first, count = lead(body)

    cited = [int(x) for x in re.findall(r'href="#note-(\d+)"', first)]
    kept = ''
    if cited:
        notes = [m.group(0) for m in NOTE.finditer(apparatus)
                 if int(m.group(1)) <= max(cited)]
        if notes:
            kept = ('\n\n<div class="apparatus" markdown="1">\n\n'
                    '<hr class="rule-major">\n\n## Notes and Sources\n\n'
                    + '\n\n'.join(notes) + '\n\n</div>\n')

    if 'gated:' not in head:
        head = head.rstrip('\n') + '\ngated: true\n'
    io.open(path, 'w', encoding='utf-8').write(
        '---\n' + head + '---\n\n' + first + '\n' + kept)
    print('%-28s %3d words, %s' % (
        path, count, 'notes 1-%d' % max(cited) if cited else 'no notes'))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        withhold(p)
