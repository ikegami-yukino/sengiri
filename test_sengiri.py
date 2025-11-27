import copy
import unittest

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
    '奇声を発しながら🦑をやっとる…': ['奇声を発しながら🦑をやっとる…'],
    '心肺停止したので寝ます。おやすみなさい。': ['心肺停止したので寝ます。', 'おやすみなさい。'],
    '大学院生「奨学金を…」': ['大学院生「奨学金を…」']
}


class TestSengiri(unittest.TestCase):

    def test_has_delimiter(self):
        self.assertTrue(sengiri.sengiri._has_delimiter('♡', '記号,一般,*,*,*,*,♡,,,,'))
        self.assertTrue(sengiri.sengiri._has_delimiter('。', '記号,句点,*,*,*,*,。,。,。'))


    def test_analyze_by_mecab(self):
        test_cases = copy.copy(TEST_CASES)
        del test_cases['大変なことになった。（後で聞いたのだが、脅されたらしい）（脅迫はやめてほしいと言っているのに）']
        for (source, expected) in test_cases.items():
            actual = sengiri.sengiri._analyze_by_mecab(source, '', 3)
            self.assertEqual(actual, expected)


    def test_tokenize(self):
        for (source, expected) in TEST_CASES.items():
            actual = sengiri.tokenize(source)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
