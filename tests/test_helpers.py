from general.book import Book
from unittest import mock
from general.constants import GATE_END_INDICATOR, CHAPTER_INDICATOR


def test_split_volumes():
    book = Book([
        p(GATE_END_INDICATOR),
        p('par - 1'),
        p('par - 2')
    ])
    assert len(book.chapters) == 1
    assert len(book.volumes) == 1

    book = Book([
        p(GATE_END_INDICATOR),
        p('par - 1'),
        p('par - 2')
    ], min_chars=3, max_chars=8)
    assert len(book.chapters) == 2
    assert len(book.volumes) == 2

    book = Book([
        p(GATE_END_INDICATOR),
        p('par - 1'),
        p('par - 2')
    ], min_chars=3, max_chars=6)
    assert len(book.chapters) == 2
    assert len(book.volumes) == 2

    book = Book([
        p(GATE_END_INDICATOR),
        p('par - 1'),
        p(CHAPTER_INDICATOR),
        p('par - 2')
    ])
    assert len(book.chapters) == 1
    assert len(book.volumes) == 1

    book = Book([
        p('par - 0'),
        p(GATE_END_INDICATOR),
        p('par - 1'),
        p(CHAPTER_INDICATOR),
        p('par - 2'),
        p('par - 3'),
        p(CHAPTER_INDICATOR),
        p('par - 4')
    ])
    assert len(book.chapters) == 2
    assert len(book.volumes) == 1

    book = Book([
        p('par - 0'),
        p('par - 1'),
        p('par - 2'),
        p(GATE_END_INDICATOR),
        p('par - 4'),
        p('par - 5'),
        p('par - 6'),
        p(CHAPTER_INDICATOR),
        p('par - 8'),
        p('par - 9'),
        p('par -10'),
        p('par -11'),
        p('par -12'),
        p('par -13'),
        p(CHAPTER_INDICATOR),
        p('par -15'),
        p('par -16'),
        p('par -17'),
        p(CHAPTER_INDICATOR),
        p('par -19'),
        p('par -20'),
        p('par -21')
    ],
        min_chars=9,
        max_chars=22
    )
    assert len(book.chapters) == 5
    assert len(book.volumes) == 5

    book = Book([
        p('par - 0'),
        p('par - 1'),
        p('par - 2'),
        p(GATE_END_INDICATOR),
        p('par - 4'),
        p(CHAPTER_INDICATOR),
        p('par - 6'),
        p('par - 7'),
        p('par - 8'),
        p('par - 9'),
        p(CHAPTER_INDICATOR),
        p('par -11'),
        p('par -12'),
        p('par -13'),
        p(CHAPTER_INDICATOR),
        p('par -15'),
        p('par -16'),
        p('par -17')
    ],
        min_chars=20,
        max_chars=40
    )
    assert len(book.chapters) == 3
    assert len(book.volumes) == 3



def p(text):
    paragraph = mock.Mock()
    paragraph.text = text
    return paragraph
