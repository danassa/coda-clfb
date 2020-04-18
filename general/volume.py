import logging


class Volume:
    def __init__(self, chars, start, end, fst_c_index_in_v, lst_c_index_in_v, first_paragraph=None, last_paragraph=None):
        """
        :param chars: total count of characters in all this volume's paragraphs
        :param start: index of the book's paragraphs which will be the FIRST in this volume
        :param end: index of the book's paragraphs which will be the LAST in this volume
        :param fst_c_index_in_v: the index of the FIRST chapter in this volume, in the book's Chapters field
        :param lst_c_index_in_v: the index of the LAST chapter in this volume, according to the book's Chapters field
        :param first_paragraph: indicate if this volume STARTS in the middle of a chapter. None or a string.
        :param last_paragraph: indicate if this volume ENDS in the middle of a chapter. None or a string.
        """
        self.start_index = start
        self.end_index = end
        self.chars = chars
        self.first_paragraph = first_paragraph
        self.last_paragraph = last_paragraph
        self.first_chapter_index = fst_c_index_in_v
        self.last_chapter_index = lst_c_index_in_v
        self.elements = None
        self.doc = None
        self.volume_num = None
        self.font = None
        self.style = None
        logging.debug("Volume initialized with paragraphs: {} to {}, chapters {} to {}, with first paragraph: '{}' and last: '{}'"
                      .format(self.start_index, self.end_index, self.first_chapter_index, self.last_chapter_index, self.first_paragraph, self.last_paragraph))

    def update_first_chapter(self, chars_added, new_first_paragraph):
        self.start_index = new_first_paragraph
        self.chars = self.chars + chars_added
        self.first_paragraph = None

    def update_last_chapter(self, chars_removed, new_last_paragraph):
        self.end_index = new_last_paragraph
        self.chars = self.chars - chars_removed
        self.last_paragraph = None
