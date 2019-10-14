import re

import emoji
import MeCab

EMOJIS = set(emoji.UNICODE_EMOJI.keys())
DELIMITERS = set({'。', '．', '…', '・・・', '...', '！',
                  '!', '？', '?', '！？', '？！', '!?', '?!'})
re_parenthesis = re.compile('([%s])([\(（][^\)）]{10,}[\)）])' % ''.join(DELIMITERS))
EMOJI_THRESHOLD = 3
LOUGHING = ('w', 'ww', 'www', 'wwww')


def _has_delimiter(surface, features):
    return (features.startswith('記号,一般,')
            or any(surface == d for d in DELIMITERS)
                or all(c in DELIMITERS for c in surface))


def _analyze_by_mecab(line, mecab_args):
    tagger = MeCab.Tagger(mecab_args)
    pairs = [l.split('\t') for l in tagger.parse(line).splitlines()[:-1]]

    result = []
    has_delimiter_flag = False
    emoji_count = 0

    for (i, (surface, features)) in enumerate(pairs):
        if surface in EMOJIS:
            emoji_count += 1
            if emoji_count >= EMOJI_THRESHOLD and i < len(pairs) and pairs[i+1][0] not in EMOJIS:
                result[-1].append(surface)
                result[-1] = ''.join(result[-1])
                result.append([])
                emoji_count = 0
                continue
        elif _has_delimiter(surface, features):
            has_delimiter_flag = True
        elif (result and result[-1] and result[-1][-1] not in ('http://', 'https://')
                and surface in LOUGHING):
            has_delimiter_flag = True
        elif has_delimiter_flag is True and surface == '.' and result[-1][-1] in LOUGHING:
            has_delimiter_flag = False
        elif has_delimiter_flag is True:
            result[-1] = ''.join(result[-1])
            result.append([])
            has_delimiter_flag = False

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
