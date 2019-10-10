import re

import MeCab

re_delimiter = re.compile('\t([…。．！？\!\?―\t\]]+)(?!\))')
re_parenthesis = re.compile('([%s])([\(（][^\)）]{10,}[\)）])' % ''.join(DELIMITERS))


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
    for line in doc.splitlines():
        tagger = MeCab.Tagger('-F %m\\t --eos-format=\n ' + mecab_args)
        segmented_words = tagger.parse(line)
        segmented_words = re_delimiter.sub(lambda x: x.group(1)+'\n', segmented_words)
        segmented_words = segmented_words.replace('\t', '')
        for l in segmented_words.splitlines():
            result.append(l)
    return result
