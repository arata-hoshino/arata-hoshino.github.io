#!/usr/bin/env python3
"""
Hold a chapter back at its first section.

    python3 tools/withhold.py _essays/on-building.md ...

What stays is everything down to the second numbered section, with the
notes that the retained text actually cites, and one line saying where to
write for the rest. Everything after that comes off the page.

Run it after tools/import_chapter.py: the importer writes the whole
chapter, and this takes it back down again.
"""

import io
import re
import sys

LINE = ('Reach out to Arata Hoshino for more details: '
        '[arata.h.hoshino@gmail.com](mailto:arata.h.hoshino@gmail.com)')

NOTE = re.compile(r'^(\d+)\. .*?(?:\n\{: #note-\1 \.note\})', re.M | re.S)


def withhold(path):
    text = io.open(path, encoding='utf-8').read()
    _, head, rest = text.split('---\n', 2)
    body, _, apparatus = rest.partition('<div class="apparatus"')

    heads = list(re.finditer(r'^## .+$', body, re.M))
    if len(heads) < 2:
        raise SystemExit('%s: only one section; nothing to hold back' % path)
    first = body[:heads[1].start()].rstrip('\n')

    # the notes the retained text still points at, which are always the
    # leading run, so the numbering they carry stays correct
    cited = [int(n) for n in re.findall(r'href="#note-(\d+)"', first)]
    kept = ''
    if cited:
        notes = [m.group(0) for m in NOTE.finditer(apparatus)
                 if int(m.group(1)) <= max(cited)]
        if notes:
            kept = ('\n\n<div class="apparatus" markdown="1">\n\n'
                    '<hr class="rule-major">\n\n## Notes and Sources\n\n'
                    + '\n\n'.join(notes) + '\n\n</div>\n')

    io.open(path, 'w', encoding='utf-8').write(
        '---\n' + head + '---\n\n' + first + '\n\n' + LINE + '\n' + kept)
    print('%-28s first section kept, %s' % (
        path, 'notes 1-%d' % max(cited) if cited else 'no notes'))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        withhold(p)
