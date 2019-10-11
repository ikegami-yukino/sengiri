import re

import emoji
import MeCab

EMOJIS = set(emoji.UNICODE_EMOJI.keys())
DELIMITERS = set({'。', '．', '…', '・・・', '...', '！',
                  '!', '？', '?', '！？', '？！', '!?', '?!'})
re_parenthesis = re.compile('([%s])([\(（][^\)）]{10,}[\)）])' % ''.join(DELIMITERS))


def _analyze_by_mecab(line, mecab_args):
    tagger = MeCab.Tagger(mecab_args)
    result = []
    has_delimiter = False
    for line in tagger.parse(line).splitlines():
        line = line.rstrip()
        if line == 'EOS':
            break

        (surface, features) = line.split('\t')

        if (features.startswith('記号,一般,')
            or surface in EMOJIS
                or any(surface == d for d in DELIMITERS)
                    or all(c in DELIMITERS for c in surface)):
            has_delimiter = True
        elif (result and result[-1][-1] not in ('http://', 'https://')
                and surface in ('w', 'www')):
            has_delimiter = True
        elif has_delimiter is True and surface == '.' and result[-1][-1] in ('w', 'www'):
            has_delimiter = False
        elif has_delimiter is True:
            has_delimiter = False
            result[-1] = ''.join(result[-1])
            result.append([])

        if not result:
            result.append([])
        result[-1].append(surface)

    result[-1] = ''.join(result[-1])
    return result


def tokenize(doc, mecab_args=''):
    """Split document into sentences

    Parameters
    ----------
    doc : str
        Document
    mecab_args : str
        Arguments for MeCab's Tagger

    Return
    ------
    list
        Sentences.
    """
    doc = re_parenthesis.sub(lambda m: m.group(1) + '\n' + m.group(2) + '\n', doc)

    result = []
    for line in filter(bool, doc.splitlines()):
        result += _analyze_by_mecab(line, mecab_args)
    return result
