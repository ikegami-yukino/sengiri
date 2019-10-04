import re

import emoji
import MeCab

EMOJIS = ''.join(emoji.UNICODE_EMOJI)
re_emoji = re.compile('([%s]{3,})(?!\))' % EMOJIS)
DELIMITERS = {'。', '．', '…', '・・・', '...', '！', '!', '？', '?'}
re_parenthesis = re.compile('(\([^！？\!\?。．・…%s]*[！？\!\?。．・…%s]+\))' % (EMOJIS, EMOJIS))
re_delimiter = re.compile('\t([…。．！？\!\?―\t]+)')


def tokenize(doc, mecab_args=''):
    doc = re_emoji.sub(lambda x: x.group(1)+'\n', doc)
    doc = re_parenthesis.sub(lambda x: '\n'+x.group(1)+'\n', doc)

    result = []
    for line in doc.splitlines():
        if all(c not in line for c in DELIMITERS):
            result.append(line)
            continue
        tagger = MeCab.Tagger('-F %m\t --eos-format=\n ' + mecab_args)
        segmented_words = tagger.parse(line).rstrip()
        segmented_words = re_delimiter.sub(lambda x: x.group(1)+'\n', segmented_words)
        for l in segmented_words.splitlines():
            result.append(l)
    return result
