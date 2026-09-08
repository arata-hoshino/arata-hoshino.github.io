#!/usr/bin/env python3
"""
Set the thesis in American spelling.

    python3 tools/american_spelling.py _essays/*.md index.md about.md

Only words that actually occur in the thesis are listed, so nothing is
changed by a rule nobody wrote. Proper names keep the spelling their owners
use: the International Labour Organization, Japan's Labour Force Survey, and
the UAE Federal Competitiveness and Statistics Centre.
"""

import io
import re
import sys

KEEP = [
    'International Labour Organization',
    'Statistics Centre',
    'The Costs of Decarbonisation',
]

WORDS = {
    # -ise / -isation
    'authorisation': 'authorization',
    'axiomatisation': 'axiomatization',
    'criticised': 'criticized',
    'criticises': 'criticizes',
    'decarbonisation': 'decarbonization',
    'destabilises': 'destabilizes',
    'economise': 'economize',
    'energisation': 'energization',
    'externalisation': 'externalization',
    'externalised': 'externalized',
    'fertiliser': 'fertilizer',
    'formalised': 'formalized',
    'generalisation': 'generalization',
    'generalise': 'generalize',
    'institutionalisation': 'institutionalization',
    'institutionalise': 'institutionalize',
    'institutionalised': 'institutionalized',
    'internationalising': 'internationalizing',
    'levelised': 'levelized',
    'maximise': 'maximize',
    'maximised': 'maximized',
    'mechanisation': 'mechanization',
    'mobilised': 'mobilized',
    'mobilises': 'mobilizes',
    'modularised': 'modularized',
    'monetisation': 'monetization',
    'monetise': 'monetize',
    'monopolised': 'monopolized',
    'optimised': 'optimized',
    'optimising': 'optimizing',
    'organisation': 'organization',
    'pantheised': 'pantheized',
    'realisations': 'realizations',
    'realised': 'realized',
    'recognise': 'recognize',
    'recognises': 'recognizes',
    'stabilise': 'stabilize',
    'standardised': 'standardized',
    'subsidised': 'subsidized',
    'urbanisation': 'urbanization',
    'utilisation': 'utilization',
    # -our
    'behaviour': 'behavior',
    'favourable': 'favorable',
    'labour': 'labor',
    'labourers': 'laborers',
    'neighbourhood': 'neighborhood',
    'unfavourable': 'unfavorable',
    # -re
    'centre': 'center',
    'centred': 'centered',
    'centres': 'centers',
    'epicentre': 'epicenter',
    'metre': 'meter',
    'metres': 'meters',
    'theatre': 'theater',
    # the rest
    'ageing': 'aging',
    'analysed': 'analyzed',
    'analyses': 'analyzes',
    'analysing': 'analyzing',
    'cancelled': 'canceled',
    'cheque': 'check',
    'cheques': 'checks',
    'defence': 'defense',
    'judgement': 'judgment',
    'judgements': 'judgments',
    'programme': 'program',
    'programmes': 'programs',
    'scepticism': 'skepticism',
    'signalling': 'signaling',
    'totalling': 'totaling',
    'traveller': 'traveler',
    'travelling': 'traveling',
}

PATTERN = re.compile(r'\b(%s)\b' % '|'.join(sorted(WORDS, key=len, reverse=True)),
                     re.IGNORECASE)


def american(text):
    held = []
    for phrase in KEEP:
        token = '\x00%d\x00' % len(held)
        held.append(phrase)
        text = text.replace(phrase, token)

    def one(m):
        word = m.group(0)
        new = WORDS[word.lower()]
        if word.isupper():
            return new.upper()
        if word[0].isupper():
            return new[0].upper() + new[1:]
        return new
    text = PATTERN.sub(one, text)

    for i, phrase in enumerate(held):
        text = text.replace('\x00%d\x00' % i, phrase)
    return text


if __name__ == '__main__':
    for path in sys.argv[1:]:
        before = io.open(path, encoding='utf-8').read()
        after = american(before)
        if after != before:
            io.open(path, 'w', encoding='utf-8').write(after)
            n = sum(1 for _ in PATTERN.finditer(before))
            print('%-52s %d' % (path, n))
