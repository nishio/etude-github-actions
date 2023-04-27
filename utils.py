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
    >>> contains_japanese_characters("A: 🟩🟩🟩🟥🟥🟥⬜⬜⬜ v.s. B: 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥")
    False
    >>> contains_japanese_characters("🤔")
    False
    """
    if japanese.search(s):
        return True
    else:
        return False


def get_body_of_line(line):
    """
    >>> get_body_of_line("  text ")
    ('  ', 'text', '')
    >>> get_body_of_line("  Q&A[gpt-4.icon][nishio.icon]")
    ('  ', 'Q&A', '[gpt-4.icon][nishio.icon]')
    >>> get_body_of_line("[nishio.icon][gpt-4.icon]Explain shortly")
    ('[nishio.icon][gpt-4.icon]', 'Explain shortly', '')
    >>> get_body_of_line("　　[GPT-4.icon]AとBの意見の違い")
    """
    indent, tail = re.match("^([ \t\u3000]*)(.*)", line).groups()
    tail = tail.rstrip()  # remove trailing spaces
    # remove icons from tail
    # regexp matches [nishio.icon] and [gpt-4.icon]
    ICON = r"\[.*?\.icon\]"
    prefix, body, postfix = re.match(
        f"^((?:{ICON})*)(.*?)((?:{ICON})*)$", tail).groups()
    return (indent + prefix, body, postfix)


if __name__ == "__main__":
    doctest.testmod()
