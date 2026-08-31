#!/usr/bin/env python3
"""
Turn a chapter of the draft into the page the site serves.

Run it over the .md files of the draft:

    python3 tools/import_chapter.py drafts/*.md

It does six things, all of them things the site's conventions require and
none of them things worth doing by hand a second time:

  * repairs the mojibake the drafts carry (en dashes, minus signs, the
    multiplication sign, and the accented names)
  * drops the draft's own byline, rule and title: the layout sets the title
  * turns the in-text references into Chicago's superscript figures, each
    one linking to the note it names
  * numbers the notes as Chicago numbers them, and anchors each
  * gathers Notes and Sources and Objections and Limits into the apparatus,
    behind the rule that closes the body
  * marks the figure slots, and sets the equations apart
"""

import io
import os
import re
import sys

# the chapters, by the name of the draft file
CHAPTERS = {
    '01_Prologue': 'prologue',
    '02_Chapter1': 'everything-is-energy-conversion',
    '03_Chapter2': 'two-endgoals-twelve-thousand-years',
    '04_Chapter3': 'a-scarcity-of-our-own-tying',
    '05_Chapter4': 'the-household-malthus',
    '06_Chapter5': 'the-abundance-cascade',
    '07_Chapter6': 'the-crisis-of-distribution',
    '08_Chapter7': 'beyond-price',
    '09_Chapter8': 'a-map-of-clusters',
    '10_Final_Chapter': 'the-stakes',
}

# the mojibake, word by word where the character is ambiguous
LITERAL = [
    ('Ã ', 'à'),          # Adserà
    ('AlÃ­', 'Alí'),      # Alícia
    ('AdserÃ', 'Adserà'),
    ('MichÃ¨le', 'Michèle'),
    ('communiquÃ©', 'communiqué'),
    ('NisÃ©n', 'Nisén'),
    ('MyrskylÃ¤', 'Myrskylä'),
    ('RÃ¸kke', 'Røkke'),
    ('YlikÃ¤nnÃ¶', 'Ylikännö'),
    ('cafÃ©', 'café'),
    ('scholÄ', 'scholē'),
    ('MahÅ', 'Mahō'),
    ('neichÄ', 'neichā'),
    ('Ãditions', 'Éditions'),
    ('Â·', '·'),
    ('Â§', '§'),
    ('Ã·', '÷'),
    # the chains and equations, where the arrow and the approximation sign
    # both came through as the same broken byte
    ('Eâ â P_Eâ â application demand Dâ â investmentâ â Eâ',
     'E↑ → P_E↓ → application demand D↑ → investment↑ → E↑'),
    ('Civilizational competitiveness C â Institutions I Ã Effective energy abundance E Ã Labour input (automation) L',
     'Civilizational competitiveness C ≈ Institutions I × Effective energy abundance E × Labour input (automation) L'),
    ('Civilizational competitiveness C â Institutions I Ã Effective energy abundance E Ã Labour input L',
     'Civilizational competitiveness C ≈ Institutions I × Effective energy abundance E × Labour input L'),
    ('C â I Ã E Ã L', 'C ≈ I × E × L'),
    ('L â Technology access T Ã Large capital K',
     'L ≈ Technology access T × Large capital K'),
    ('L â T Ã K', 'L ≈ T × K'),
    ('n\\* â g(', 'n\\* ≈ g('),
    ('n* â g(', 'n* ≈ g('),
]

# the arrow chain of 4.4, written across one line
ARROW_LINE = re.compile(r'^(> .*?)$', re.M)


def repair(text):
    for old, new in LITERAL:
        text = text.replace(old, new)

    # a chain of arrows inside a single blockquote line
    def arrows(m):
        line = m.group(0)
        if line.count(' â ') >= 2:
            return line.replace(' â ', ' → ')
        return line
    text = ARROW_LINE.sub(arrows, text)

    # ranges: 1910–60, S279–S288, 1253b–1254a
    text = re.sub(r'(?<=[0-9A-Za-z])â(?=[0-9A-Za-z])', '–', text)
    # a negative number
    text = re.sub(r'â(?=[0-9])', '−', text)
    # what is left of the multiplication sign
    text = text.replace(' Ã ', ' × ')
    # the drafts use the Japanese approximation sign; the site sets the
    # one English typography uses
    text = text.replace('≒', '≈')
    return text


def strip_front(text):
    """Drop the draft's byline, its rule, and its own title line."""
    text = re.sub(r'^\*Arata Hoshino \| [^\n]*\*\n+', '', text)
    text = re.sub(r'^---\n+', '', text)
    text = re.sub(r'^#\s+[^\n]*\n+', '', text)
    return text


FIGURE = re.compile(
    r'(?:^> \*\*\[Figure ([0-9]+-[0-9]+)\]\s*(.*?)\*\*[^\n]*\n(?:^>[^\n]*\n)*)+',
    re.M)


def figures(body):
    """Mark each figure slot with its number, title and caption."""

    def one(block):
        lines = [re.sub(r'^>\s?', '', l) for l in block.strip('\n').split('\n')]
        out, cur = [], None
        for line in lines:
            m = re.match(r'\*\*\[Figure ([0-9]+-[0-9]+)\]\s*(.*?)\*\*\s*(.*)$', line)
            if m:
                if cur:
                    out.append(cur)
                cur = {'n': m.group(1), 'title': m.group(2), 'caption': []}
                if m.group(3).strip():
                    cur['caption'].append(m.group(3).strip())
            elif cur is not None and line.strip():
                cur['caption'].append(line.strip())
        if cur:
            out.append(cur)

        html = []
        for f in out:
            html.append('<div class="figure-callout">')
            html.append('  <p class="figure-title">Figure %s · %s</p>' % (f['n'], f['title']))
            if f['caption']:
                html.append('  <p class="figure-caption">%s</p>' % ' '.join(f['caption']))
            html.append('</div>')
        return '\n'.join(html) + '\n'

    return FIGURE.sub(lambda m: one(m.group(0)), body)


EQUATION = re.compile(r'^> \*\*(.+?)\*\*\s*$', re.M)


def equations(body):
    """A blockquote that states a relation is set apart as one."""
    def one(m):
        inner = m.group(1)
        if any(c in inner for c in ('≈', '→', '=', '÷')):
            # the paragraph is raw html, so the markdown escapes come out
            inner = inner.replace('\\*', '*').replace('\\_', '_')
            return '<p class="equation">%s</p>' % inner
        return m.group(0)
    return EQUATION.sub(one, body)


def references(body):
    """Chicago's superscript, after the punctuation, linking to the note."""
    def sup(m):
        n, punct = m.group(1), m.group(2)
        return '%s<sup class="noteref"><a href="#note-%s">%s</a></sup>' % (punct, n, n)
    return re.sub(r'[ \n]*\[(\d+)\]([.,;:]?)', sup, body)


def notes(app):
    """Number the notes, and give each one an anchor."""
    out, pending = [], None
    for line in app.split('\n'):
        m = re.match(r'^\*\*\[(\d+)\] ', line)
        if m:
            pending = m.group(1)
            line = re.sub(r'^\*\*\[(\d+)\] ', r'**\1. ', line)
        elif pending and line.strip() == '':
            out.append('{: #note-%s .note}' % pending)
            pending = None
        out.append(line)
    return '\n'.join(out)


def links(text):
    """A bare URL in the notes becomes a link on its host."""
    def one(m):
        url = m.group(0).rstrip('.,;')
        tail = m.group(0)[len(url):]
        host = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
        return '[%s](%s){:target="_blank" rel="noopener"}%s' % (host, url, tail)
    return re.sub(r'https?://[^\s)\]]+', one, text)


def convert(path):
    stem = os.path.basename(path)
    key = next((k for k in CHAPTERS if stem.startswith(k)), None)
    if key is None:
        raise SystemExit('no chapter matches %s' % stem)
    slug = CHAPTERS[key]

    text = repair(io.open(path, encoding='utf-8').read())
    text = strip_front(text)

    # the apparatus opens at Notes and Sources
    m = re.search(r'^---\n+## (?:[^\n]*: )?Notes and Sources\s*$', text, re.M)
    if not m:
        raise SystemExit('%s: no Notes and Sources' % stem)
    body, app = text[:m.start()], text[m.start():]

    body = figures(body)
    body = equations(body)
    body = references(body)

    app = re.sub(r'^---\n+## (?:[^\n]*: )?(Notes and Sources|Objections and Limits)\s*$',
                 r'<hr class="rule-major">\n\n## \1', app, flags=re.M)
    app = notes(app)
    # the objections cite the notes too; by now the notes' own leads are
    # numbered rather than bracketed, so nothing here is caught twice
    app = references(app)
    app = links(app)
    app = '<div class="apparatus" markdown="1">\n\n' + app.strip('\n') + '\n\n</div>\n'

    # keep the front matter the site already carries for this chapter
    target = '_essays/%s.md' % slug
    head = io.open(target, encoding='utf-8').read().split('---\n')[1]
    io.open(target, 'w', encoding='utf-8').write(
        '---\n' + head + '---\n\n' + body.strip('\n') + '\n\n' + app)
    print('%-24s -> %s' % (stem, target))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        convert(p)
