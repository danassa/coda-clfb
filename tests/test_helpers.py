from general.book import Book
from general.element import Element
from unittest import mock
from general.constants import GATE_END_INDICATOR, CHAPTER_INDICATOR

def test_calc_min_chars_per_last_volume():
    book = Book([e_p(GATE_END_INDICATOR), e_p('1'), e_p('2')], 3000, 5000)
    min_per_last = book.calc_min_chars_per_last_volume()
    assert min_per_last == 2000

def test_split_volumes():
    book = Book([
        e_p(GATE_END_INDICATOR),
        e_p('par - 1'),
        e_p('par - 2')
    ])
    assert len(book.chapters) == 1
    assert len(book.volumes) == 1

    book = Book([
        e_p(GATE_END_INDICATOR),
        e_p('par - 1'),
        e_p('par - 2')
    ], min_chars=3, max_chars=8)
    assert len(book.chapters) == 2
    assert len(book.volumes) == 2

    book = Book([
        e_p(GATE_END_INDICATOR),
        e_p('par - 1'),
        e_p('par - 2')
    ], min_chars=3, max_chars=6)
    assert len(book.chapters) == 2
    assert len(book.volumes) == 2

    book = Book([
        e_p(GATE_END_INDICATOR),
        e_p('par - 1'),
        e_p(CHAPTER_INDICATOR),
        e_p('par - 2')
    ])
    assert len(book.chapters) == 1
    assert len(book.volumes) == 1

    book = Book([
        e_p('par - 0'),
        e_p(GATE_END_INDICATOR),
        e_p('par - 1'),
        e_p(CHAPTER_INDICATOR),
        e_p('par - 2'),
        e_p('par - 3'),
        e_p(CHAPTER_INDICATOR),
        e_p('par - 4')
    ])
    assert len(book.chapters) == 2
    assert len(book.volumes) == 1

    book = Book([
        e_p('par - 0'),
        e_p('par - 1'),
        e_p('par - 2'),
        e_p(GATE_END_INDICATOR),
        e_p('par - 4'),
        e_p('par - 5'),
        e_p('par - 6'),
        e_p(CHAPTER_INDICATOR),
        e_p('par - 8'),
        e_p('par - 9'),
        e_p('par -10'),
        e_p('par -11'),
        e_p('par -12'),
        e_p('par -13'),
        e_p(CHAPTER_INDICATOR),
        e_p('par -15'),
        e_p('par -16'),
        e_p('par -17'),
        e_p(CHAPTER_INDICATOR),
        e_p('par -19'),
        e_p('par -20'),
        e_p('par -21')
    ],
        min_chars=9,
        max_chars=22
    )
    assert len(book.chapters) == 5
    assert len(book.volumes) == 5

    book = Book([
        e_p('par - 0'),
        e_p('par - 1'),
        e_p('par - 2'),
        e_p(GATE_END_INDICATOR),
        e_p('par - 4'),
        e_p(CHAPTER_INDICATOR),
        e_p('par - 6'),
        e_p('par - 7'),
        e_p('par - 8'),
        e_p('par - 9'),
        e_p(CHAPTER_INDICATOR),
        e_p('par -11'),
        e_p('par -12'),
        e_p('par -13'),
        e_p(CHAPTER_INDICATOR),
        e_p('par -15'),
        e_p('par -16'),
        e_p('par -17')
    ],
        min_chars=20,
        max_chars=40
    )
    assert len(book.chapters) == 3
    assert len(book.volumes) == 3


def e_p(text):
    return Element(True, p(text))


def p(text):
    paragraph = mock.Mock()
    paragraph.text = text
    return paragraph
