import copy

from nose.tools import assert_equal, assert_true
import sengiri.sengiri

TEST_CASES = {
    'うーん🤔🤔🤔どうしよう': ['うーん🤔🤔🤔', 'どうしよう'],
    'モー娘。のコンサートに行った。': ['モー娘。のコンサートに行った。'],
    '楽しかったし嬉しかった。すごく充実した!': ['楽しかったし嬉しかった。', 'すごく充実した!'],
    'ありがとう＾＾ 助かります。': ['ありがとう＾＾', '助かります。'],
    '大変なことになった。（後で聞いたのだが、脅されたらしい）（脅迫はやめてほしいと言っているのに）':
        ['大変なことになった。', '（後で聞いたのだが、脅されたらしい）', '（脅迫はやめてほしいと言っているのに）'],
    '楽しかったw また遊ぼwww': ['楽しかったw', 'また遊ぼwww'],
    'http://www.inpaku.go.jp/': ['http://www.inpaku.go.jp/'],
    '機械学習と統計的推論と微分幾何と関数解析と統計力学の動画！😎✌️':
        ['機械学習と統計的推論と微分幾何と関数解析と統計力学の動画！😎✌️'],
    '奇声を発しながら🦑をやっとる…': ['奇声を発しながら🦑をやっとる…']
}


def test_has_delimiter():
    assert_true(sengiri.sengiri._has_delimiter('♡', '記号,一般,*,*,*,*,♡,,,,'))
    assert_true(sengiri.sengiri._has_delimiter('。', '記号,句点,*,*,*,*,。,。,。'))


def test_analyze_by_mecab():
    test_cases = copy.copy(TEST_CASES)
    del test_cases['大変なことになった。（後で聞いたのだが、脅されたらしい）（脅迫はやめてほしいと言っているのに）']
    for (source, expected) in test_cases.items():
        actual = sengiri.sengiri._analyze_by_mecab(source, '', 3)
        assert_equal(actual, expected)


def test_tokenize():
    for (source, expected) in TEST_CASES.items():
        actual = sengiri.tokenize(source)
        assert_equal(actual, expected)
