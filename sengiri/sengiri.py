import re

import emoji
import MeCab

EMOJIS = set(emoji.UNICODE_EMOJI.keys())
DELIMITERS = set({'。', '．', '…', '・・・', '...', '！', '!', '？', '?',
                  '！？', '？！', '!?', '?!'})
OPEN_BRACKETS = '｢「(（[［【『〈《〔｛{«‹〖〘〚'
CLOSE_BRACKETS = '｣」)）]］】』〉》〕｝}»›〗〙〛'
BRACKETS = set(OPEN_BRACKETS) | set(CLOSE_BRACKETS)
LOUGHING = ('w', 'ww', 'www', 'wwww')
re_parenthesis = None
prev_parenthesis_threshold = 0


def _has_delimiter(surface, features):
    return ((features.startswith('記号,一般,') and surface not in BRACKETS)
            or any(surface == d for d in DELIMITERS)
                or all(c in DELIMITERS for c in surface))


def _analyze_by_mecab(line, mecab_args, emoji_threshold):
    tagger = MeCab.Tagger(mecab_args)
    pairs = [l.split('\t') for l in tagger.parse(line).splitlines()[:-1]]

    result = [[]]
    has_delimiter_flag = False
    emoji_count = 0

    for (i, (surface, features)) in enumerate(pairs[:-1]):
        if all(c in EMOJIS for c in surface):
            emoji_count += len(surface)
            if result and emoji_count >= emoji_threshold and pairs[i+1][0] not in EMOJIS:
                result[-1].append(surface)
                result[-1] = ''.join(result[-1])
                result.append([])
                emoji_count = 0
                continue
        elif surface in BRACKETS:
            has_delimiter_flag = False
        elif _has_delimiter(surface, features):
            has_delimiter_flag = True

        # Check www is not in a part of URL
        elif (result and result[-1] and result[-1][-1] not in ('http://', 'https://')
                and surface in LOUGHING):
            has_delimiter_flag = True
        elif has_delimiter_flag is True and surface == '.' and result[-1][-1] in LOUGHING:
            has_delimiter_flag = False

        elif has_delimiter_flag is True:
            result[-1] = ''.join(result[-1])
            result.append([])
            has_delimiter_flag = False

        result[-1].append(surface)

    result[-1].append(pairs[-1][0])
    result[-1] = ''.join(result[-1])
    return result


def tokenize(doc, mecab_args='', emoji_threshold=3, parenthesis_threshold=10):
    """Split document into sentences

    Parameters
    ----------
    doc : str
        Document
    mecab_args : str
        Arguments for MeCab's Tagger
    emoji_threshold : int
        The numbers of emoji as sentence delimiter
    parenthesis_threshold : int
        The numbers of characters in parenthesis to delimit doc

    Return
    ------
    list
        Sentences.
    """
    global re_parenthesis, prev_parenthesis_threshold

    if prev_parenthesis_threshold != parenthesis_threshold:
        prev_parenthesis_threshold = parenthesis_threshold
        re_parenthesis = re.compile('([%s])([%s][^%s]{%s,}[%s])'
                                    % (''.join(DELIMITERS), re.escape(OPEN_BRACKETS),
                                       re.escape(CLOSE_BRACKETS), parenthesis_threshold,
                                       re.escape(CLOSE_BRACKETS)))

    doc = re_parenthesis.sub(lambda m: m.group(1) + '\n' + m.group(2) + '\n', doc)

    result = []
    for line in filter(bool, doc.splitlines()):
        result += _analyze_by_mecab(line, mecab_args, emoji_threshold)
    return result
