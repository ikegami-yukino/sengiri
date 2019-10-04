from nose.tools import assert_equal
import sengiri

def test_tokenize():
    actual = sengiri.tokenize('これは！(すばらしい！)感動……。')
    assert_equal(actual, ['これは！', '(すばらしい！)', '感動……。'])
    actual = sengiri.tokenize('うーん🤔🤔🤔どうしよう')
    assert_equal(actual, ['うーん🤔🤔🤔', 'どうしよう'])
    actual = sengiri.tokenize('モー娘。のコンサートに行った。')
    assert_equal(actual, ['モー娘。のコンサートに行った。'])
    actual = sengiri.tokenize('楽しかったし嬉しかった。すごく充実した!')
    assert_equal(actual, ['楽しかったし嬉しかった。', 'すごく充実した!'])
