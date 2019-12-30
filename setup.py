# -*- coding: utf-8 -*-
from codecs import open
import os
import pkgutil
import re
from setuptools import setup

install_requires = ['emoji'] if pkgutil.find_loader('MeCab') else ['emoji', 'mecab']

with open(os.path.join('sengiri', '__init__.py'), 'r', encoding='utf8') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

setup(
    name='sengiri',
    packages=['sengiri'],
    version=version,
    license='MIT License',
    platforms=['POSIX', 'Windows', 'Unix', 'MacOS'],
    description='Yet another sentence-level tokenizer for the Japanese text',
    author='Yukino Ikegami',
    author_email='yknikgm@gmail.com',
    url='https://github.com/ikegami-yukino/sengiri',
    keywords=['japanese', 'tokenizer', 'sentence', 'sentence-tokenizer'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing'
        ],
    long_description='%s\n\n%s' % (open('README.rst', encoding='utf8').read(),
                                   open('CHANGES.rst', encoding='utf8').read()),
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector'
)
