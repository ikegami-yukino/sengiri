sengiri
==========
|travis| |coveralls| |pyversion| |version| |license|

sengiri is yet another sentence-level tokenizer for the Japanese text

Dependencies
==============

MeCab

INSTALLATION
==============

::

 $ pip install sengiri


USAGE
============

.. code:: python

  import sengiri

  print(sengiri.tokenize('これは！(すばらしい！)感動……。'))
  #=>['これは！', '(すばらしい！)', '感動……。']
  print(sengiri.tokenize('うーん🤔🤔🤔どうしよう'))
  #=>['うーん🤔🤔🤔', 'どうしよう']
  print(sengiri.tokenize('モー娘。のコンサートに行った。'))
  #=>['モー娘。のコンサートに行った。']


.. |travis| image:: https://travis-ci.org/ikegami-yukino/sengiri.svg?branch=master
    :target: https://travis-ci.org/ikegami-yukino/sengiri
    :alt: travis-ci.org

.. |coveralls| image:: https://coveralls.io/repos/ikegami-yukino/sengiri/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ikegami-yukino/sengiri?branch=master
    :alt: coveralls.io

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/sengiri.svg

.. |version| image:: https://img.shields.io/pypi/v/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: license
