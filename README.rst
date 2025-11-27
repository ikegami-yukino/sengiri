sengiri
==========
|pyversion| |version| |license| |download| |nowarnonukes|

Yet another sentence-level tokenizer for the Japanese text

DEPENDENCIES
==============

- MeCab
- emoji

INSTALLATION
==============

::

 $ pip install sengiri


USAGE
============

.. code:: python

  import sengiri

  print(sengiri.tokenize('うーん🤔🤔🤔どうしよう'))
  #=>['うーん🤔🤔🤔', 'どうしよう']
  print(sengiri.tokenize('モー娘。のコンサートに行った。'))
  #=>['モー娘。のコンサートに行った。']
  print(sengiri.tokenize('ありがとう＾＾ 助かります。'))
  #=>['ありがとう＾＾', '助かります。']
  print(sengiri.tokenize('顔文字テスト(*´ω｀*)うまくいくかな？'))
  #=>['顔文字テスト(*´ω｀*)うまくいくかな？']
  # I recommend using the NEologd dictionary.
  print(sengiri.tokenize('顔文字テスト(*´ω｀*)うまくいくかな？', mecab_args='-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'))
  #=>['顔文字テスト(*´ω｀*)', 'うまくいくかな？']
  print(sengiri.tokenize('子供が大変なことになった。'
                         '（後で聞いたのだが、脅されたらしい）'
                         '（脅迫はやめてほしいと言っているのに）'))
  #=>['子供が大変なことになった。', '（後で聞いたのだが、脅されたらしい）', '（脅迫はやめてほしいと言っているのに）']
  print(sengiri.tokenize('楽しかったw また遊ぼwww'))
  #=>['楽しかったw', 'また遊ぼwww']
  print(sengiri.tokenize('http://www.inpaku.go.jp/'))
  #=>['http://www.inpaku.go.jp/']


.. |pyversion| image:: https://img.shields.io/pypi/pyversions/sengiri.svg

.. |version| image:: https://img.shields.io/pypi/v/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: license

.. |download| image:: https://static.pepy.tech/personalized-badge/sengiri?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/sengiri
    :alt: download

.. |nowarnonukes| image:: https://img.shields.io/badge/NO%20WAR-NO%20NUKES-brightgreen
    :alt: NO WAR
