from docx import Document
import logging
from general.constants import *


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
        self.start_paragraph_index = start
        self.end_paragraph_index = end
        self.chars = chars
        self.first_paragraph = first_paragraph
        self.last_paragraph = last_paragraph
        self.first_chapter = fst_c_index_in_v
        self.last_chapter = lst_c_index_in_v
        self.doc = None
        self.volume_num = None
        logging.debug("Volume initialized with paragraphs: {} to {}, chapters {} to {}, with first paragraph: '{}' and last: '{}'"
                      .format(self.start_paragraph_index, self.end_paragraph_index, self.first_chapter, self.last_chapter, self.first_paragraph, self.last_paragraph))

    def update_first_chapter(self, chars_added, new_first_paragraph):
        self.start_paragraph_index = new_first_paragraph
        self.chars = self.chars + chars_added
        self.first_paragraph = None

    def update_last_chapter(self, chars_removed, new_last_paragraph):
        self.end_paragraph_index = new_last_paragraph
        self.chars = self.chars - chars_removed
        self.last_paragraph = None

    def create_doc(self, path, gate_index, volume_num, last_volume_num):
        self.doc = Document(path)
        self.volume_num = volume_num

        self.remove_redundant_paragraph(gate_index)
        self.delete_chapter_beginning_markers()
        self.add_split_chapter_notes(gate_index)
        if volume_num == last_volume_num:
            self.add_book_suffix()
        else:
            self.add_volume_suffix()
        self.update_first_page(last_volume_num)

    def remove_redundant_paragraph(self, gate_index):
        last_paragraph_in_book_index = len(self.doc.paragraphs) - 1
        for p in range(last_paragraph_in_book_index, self.end_paragraph_index, -1):
            self.delete_paragraph(self.doc.paragraphs[p])
        for p in range(self.start_paragraph_index - 1, gate_index, -1):
            self.delete_paragraph(self.doc.paragraphs[p])
        logging.debug("deleting paragraphs {}-{} and {}-{} in volume {}"
                      .format(self.end_paragraph_index, last_paragraph_in_book_index, gate_index, self.start_paragraph_index, self.volume_num))

    def delete_paragraph(self, paragraph):
        p = paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None

    def delete_chapter_beginning_markers(self):
        for p in self.doc.paragraphs:
            if p.text == CHAPTER_INDICATOR:
                p.text = ''

    def add_split_chapter_notes(self, gate_index):
        if self.first_paragraph is not None:
            self.doc.paragraphs[gate_index + 1].insert_paragraph_before(self.first_paragraph)
            self.doc.paragraphs[gate_index + 2].insert_paragraph_before('')
        if self.last_paragraph is not None:
            self.doc.add_paragraph('')
            self.doc.add_paragraph(self.last_paragraph)

    def add_volume_suffix(self):
        self.doc.add_paragraph('')
        last_paragraph = '{}{}'.format(END, VOLUMES_NAMES_1[self.volume_num - 1])
        self.doc.add_paragraph(last_paragraph)

    def add_book_suffix(self):
        last_non_empty_paragraph = None
        index = len(self.doc.paragraphs) - 1
        while last_non_empty_paragraph is None and index >= 0 :
            if self.doc.paragraphs[index].text != '':
                last_non_empty_paragraph = index
            index -= 1

        if self.doc.paragraphs[last_non_empty_paragraph].text != BOOK_SUFFIX:
            self.doc.add_paragraph('')
            self.doc.add_paragraph(BOOK_SUFFIX)
            logging.debug("last paragraph in the book was not '{}', adding the phrase".format(BOOK_SUFFIX))

    def update_first_page(self, last_volume_num):
        index = None
        for i in range(30, 1, -1):
            if self.doc.paragraphs[i].text == FIRST_PAGE_VOLUMES_PARAGRAPH:
                index = i
        if index is not None:
            self.doc.paragraphs[index].text = VOLUMES_NAMES_1[self.volume_num - 1]
            self.doc.paragraphs[index - 1].text = VOLUMES_NAMES_2[last_volume_num - 1]
        else:
            logging.error("couldn't locate the phrase {} in the first 30 paragraphs. "
                          "cannot update the first page with number of volumes".format(FIRST_PAGE_VOLUMES_PARAGRAPH))

