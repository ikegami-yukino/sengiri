from nose.tools import assert_equal
import sengiri

def test_tokenize():
    actual = sengiri.tokenize('うーん🤔🤔🤔どうしよう')
    assert_equal(actual, ['うーん🤔🤔🤔', 'どうしよう'])
    actual = sengiri.tokenize('モー娘。のコンサートに行った。')
    assert_equal(actual, ['モー娘。のコンサートに行った。'])
    actual = sengiri.tokenize('楽しかったし嬉しかった。すごく充実した!')
    assert_equal(actual, ['楽しかったし嬉しかった。', 'すごく充実した!'])
    actual = sengiri.tokenize('ありがとう＾＾ 助かります。')
    assert_equal(actual, ['ありがとう＾＾', '助かります。'])
    actual = sengiri.tokenize('子供が大変なことになった。'
                              '（後で聞いたのだが、脅されたらしい）'
                              '（脅迫はやめてほしいと言っているのに）')
    assert_equal(actual, ['子供が大変なことになった。',
                          '（後で聞いたのだが、脅されたらしい）',
                          '（脅迫はやめてほしいと言っているのに）'])
    actual = sengiri.tokenize('楽しかったw また遊ぼwww')
    assert_equal(actual, ['楽しかったw', 'また遊ぼwww'])
    actual = sengiri.tokenize('http://www.inpaku.go.jp/')
    assert_equal(actual, ['http://www.inpaku.go.jp/'])
