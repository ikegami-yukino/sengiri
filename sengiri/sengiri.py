import os
import re
import shutil
import subprocess
from collections.abc import Sequence
from typing import Optional, Union

import emoji
import MeCab  # type: ignore

EMOJIS: set[str] = set(emoji.unicode_codes.EMOJI_DATA.keys())
DELIMITERS: set[str] = set(
    {"。", "．", "…", "・・・", "...", "！", "!", "？", "?", "！？", "？！", "!?", "?!"}
)
OPEN_BRACKETS: str = "｢「(（[［【『〈《〔｛{«‹〖〘〚"
CLOSE_BRACKETS: str = "｣」)）]］】』〉》〕｝}»›〗〙〛"
BRACKETS: set[str] = set(OPEN_BRACKETS) | set(CLOSE_BRACKETS)
LAUGHING = ("w", "ww", "www", "wwww")
re_url_pattern: re.Pattern = re.compile(r"https?://[a-zA-Z\d/:%#\$&\?\(\)~\.=\+\-]+")
re_parenthesis: Optional[re.Pattern] = None
prev_parenthesis_threshold: int = 0

HOME_BREW_MECABRC_PATH: str = "/opt/homebrew/etc/mecabrc"
APT_MECABRC_PATH: str = "/etc/mecabrc"
DEFAULT_MECABRC_PATH: str = "/usr/local/etc/mecabrc"
MECAB_PY3_RC_ERROR_MSG: str = (
    '\nPlease specify the "mecabrc" file with the -r option in "mecab_args". '
    'For example, "-r {}".'.format(DEFAULT_MECABRC_PATH)
)


def _create_macab_tagger(mecab_args: str) -> MeCab.Tagger:
    try:
        if "-r" not in mecab_args:
            if os.getenv("MECABRC"):
                mecab_args += " -r " + os.environ["MECABRC"]
            elif shutil.which("mecab-config"):
                mecab_conf_dir = subprocess.run(["mecab-config", "--sysconfdir"],
                                                 check=True, stdout=subprocess.PIPE).stdout.decode().strip()
                mecab_args += " -r " + mecab_conf_dir + "/mecabrc"
            elif not os.path.exists(DEFAULT_MECABRC_PATH):
                if os.path.exists(HOME_BREW_MECABRC_PATH):
                    mecab_args += " -r " + HOME_BREW_MECABRC_PATH
                elif os.path.exists(APT_MECABRC_PATH):
                    mecab_args += " -r " + APT_MECABRC_PATH
        tagger = MeCab.Tagger(mecab_args)
    except RuntimeError as e:
        message = str(e)
        if ("[ifs] no such file or directory:" in message) and (message.rstrip().endswith("/mecabrc")):
            message += MECAB_PY3_RC_ERROR_MSG
            raise RuntimeError(message)
        else:
            raise e
    except Exception as e:
            raise e
    return tagger


def _partial_parse(tagger: MeCab.Tagger, constraints: Sequence[Union[Sequence[str], str]]) -> str:
    tagger.set_partial(True)
    text = ""
    for constraint in constraints:
        if isinstance(constraint, str):
            text += constraint
        else:
            text += constraint[0]
            if len(constraint) > 1:
                text += "\t" + constraint[1]
        text += "\n"
    result = tagger.parse(text).rstrip()
    tagger.set_partial(False)
    return result


def _find_url_positions(text: str) -> list[dict[str, int]]:
    matches = re_url_pattern.finditer(text)
    results = []
    for match in matches:
        results.append({
            "start": match.start(),
            "end": match.end()
        })
    return results

def _has_delimiter(surface: str, features: str) -> bool:
    return ((features.startswith("記号,一般,") and surface not in BRACKETS)
            or any(surface == d for d in DELIMITERS)
                or all(c in DELIMITERS for c in surface))


def _analyze_by_mecab(line: str, mecab_args: str, emoji_threshold: int) -> list[str]:
    tagger: MeCab.Tagger = _create_macab_tagger(mecab_args)
    parsed_text: str

    # Handle URLs
    url_positions: list[dict[str, int]] = _find_url_positions(line)
    if url_positions:
        constraints: list[Sequence[str] | str] = []
        last_pos: int = 0
        for url_pos in url_positions:
            if last_pos < url_pos["start"]:
                constraints.append(line[last_pos:url_pos["start"]])
            constraints.append([line[url_pos["start"]:url_pos["end"]], "記号,一般,*,*,*,*,*"])
            last_pos = url_pos["end"]
        if last_pos < len(line):
            constraints.append(line[last_pos:len(line)])
        parsed_text = _partial_parse(tagger, constraints)
    else:
        parsed_text = tagger.parse(line)

    pairs: list[list[str]] = [l.split("\t") for l in parsed_text.splitlines()[:-1]]

    sentence: str = ""
    result: list[str] = []
    has_delimiter_flag: bool = False
    emoji_count: int = 0

    for (i, (surface, features)) in enumerate(pairs[:-1]):
        if all(c in EMOJIS for c in surface):
            emoji_count += len(surface)
            if sentence and emoji_count >= emoji_threshold and pairs[i+1][0] not in EMOJIS:
                sentence += surface
                result.append(sentence)
                sentence = ""
                emoji_count = 0
                continue
        elif surface in BRACKETS:
            has_delimiter_flag = False
        elif _has_delimiter(surface, features):
            has_delimiter_flag = True
        elif surface in LAUGHING:
            has_delimiter_flag = True
        elif has_delimiter_flag is True and surface == "." and sentence.endswith(LAUGHING):
            has_delimiter_flag = False
        elif has_delimiter_flag is True:
            result.append(sentence)
            sentence = ""
            has_delimiter_flag = False

        sentence += surface

    sentence += pairs[-1][0]
    result.append(sentence)
    return result


def tokenize(doc: str, mecab_args: str = "", emoji_threshold: int = 3,
             parenthesis_threshold: int = 10) -> list[str]:
    """Split document into sentences

    Parameters
    ----------
    doc : str
        Document
    mecab_args : str
        Arguments for MeCab"s Tagger
    emoji_threshold : int
        The numbers of emoji as sentence delimiter
    parenthesis_threshold : int
        The numbers of characters in parenthesis to delimit doc

    Return
    ------
    list
        Sentences.
    """
    global re_parenthesis, prev_parenthesis_threshold

    if prev_parenthesis_threshold != parenthesis_threshold:
        prev_parenthesis_threshold = parenthesis_threshold
        re_parenthesis = re.compile("([%s])([%s][^%s]{%s,}[%s])"
                                    % ("".join(DELIMITERS), re.escape(OPEN_BRACKETS),
                                       re.escape(CLOSE_BRACKETS), parenthesis_threshold,
                                       re.escape(CLOSE_BRACKETS)))

    assert re_parenthesis is not None
    doc = re_parenthesis.sub(lambda m: m.group(1) + "\n" + m.group(2) + "\n", doc)

    result: list[str] = []
    for line in filter(bool, doc.splitlines()):
        result += _analyze_by_mecab(line, mecab_args, emoji_threshold)
    return result
