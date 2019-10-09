import re

import emoji
import MeCab

EMOJIS = ''.join(emoji.UNICODE_EMOJI.keys())
EMOJI_SET = set(EMOJIS)
re_emoji = re.compile('\t([%s\t]{3,})(?![\)）])' % (EMOJIS))
re_parenthesis = re.compile('([\(（][^！？\!\?。．・…]*[！？\!\?。．・…]+[\)）])')
re_delimiter = re.compile('\t([…。．！？\!\?―\t\]]+)(?!\))')


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
    doc = re_parenthesis.sub(lambda x: '\n'+x.group(1)+'\n', doc)

    result = []
    for line in doc.splitlines():
        tagger = MeCab.Tagger('-F %m\\t --eos-format=\n ' + mecab_args)
        segmented_words = tagger.parse(line)
        segmented_words = re_delimiter.sub(lambda x: x.group(1)+'\n', segmented_words)
        if any(c in EMOJI_SET for c in segmented_words):
            segmented_words = re_emoji.sub(lambda x: x.group(1)+'\n', segmented_words)
        segmented_words = segmented_words.replace('\t', '')
        for l in segmented_words.splitlines():
            result.append(l)
    return result
