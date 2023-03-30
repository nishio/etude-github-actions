import doctest
import re
# hiragana = re.compile(r'[\u3040-\u309F]')
# katakana = re.compile(r'[\u30A0-\u30FF]')
# kanji = re.compile(r'[\u4E00-\u9FFF]')
japanese = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')


def contains_japanese_characters(s):
    """
    >>> contains_japanese_characters("English")
    False
    >>> contains_japanese_characters("ひらがな")
    True
    >>> contains_japanese_characters("カタカナ")
    True
    >>> contains_japanese_characters("漢字")
    True
    """
    if japanese.search(s):
        return True
    else:
        return False


if __name__ == "__main__":
    doctest.testmod()
