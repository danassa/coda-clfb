from general.constants import *
import logging
from general.volume import Volume
from general.chapter import Chapter


class Book:

    def __init__(self, paragraphs, min_chars=MIN_CHARS_PER_VOLUME, max_chars=MAX_CHARS_PER_VOLUME):
        logging.info("book initialization began. a volume will contain {} to {} characters".format(min_chars, max_chars))
        assert min_chars <= max_chars, "minimum characters per volume must be equal or greater than the maximum"

        self.paragraphs = paragraphs
        self.min_chars_per_volume = min_chars
        self.max_chars_per_volume = max_chars
        self.last_gate_paragraph = None
        self.chapters = []
        self.chars = None
        self.volumes = []

        self.find_gate_end()
        self.create_chapters()
        self.split_volumes()

        assert self.last_gate_paragraph is not None, "no copyright paragraph found!"
        assert len(self.chapters) >= 1
        assert len(self.volumes) >= 1

    def find_gate_end(self):
        for index, paragraph in enumerate(self.paragraphs):
            if paragraph.text.startswith(GATE_END_INDICATOR):
                self.last_gate_paragraph = index + 1
                return
        logging.error("no copyright paragraph found! cannot distinguish between gate pages and the rest of the content")

    def create_chapters(self):
        total_chars = 0
        chapter_chars = 0
        current_chapter_start_index = self.last_gate_paragraph + 1

        for index, paragraph in enumerate(self.paragraphs):
            if paragraph.text == CHAPTER_INDICATOR:
                if current_chapter_start_index == self.last_gate_paragraph + 1:  # first chapter!
                    current_chapter_start_index = index + 1
                else:
                    new_chapter = Chapter(chapter_chars, current_chapter_start_index, index - 1)
                    self.chapters.append(new_chapter)
                    total_chars += chapter_chars
                    chapter_chars = 0
                    current_chapter_start_index = index + 1
            elif index > self.last_gate_paragraph:
                chapter_chars += len(paragraph.text)

        total_chars += chapter_chars
        last_chapter = Chapter(chapter_chars, current_chapter_start_index, index)
        self.chapters.append(last_chapter)
        self.chars = total_chars
        logging.info("Found {} actual chapters in the book, with a total of {} characters"
                     .format(len(self.chapters), self.chars))

    def split_volumes(self):
        c_index = 0
        v_chars = 0
        v_index = self.last_gate_paragraph + 1
        v_paragraph = None

        while True:
            try:
                chapter = self.chapters[c_index]
            except IndexError:
                if v_chars > 0:
                    self.volumes.append(Volume(v_index, self.chapters[c_index-1].end_paragraph_index, v_paragraph, None))
                break

            if v_chars + chapter.chars > self.max_chars_per_volume and v_chars > self.min_chars_per_volume:
                self.volumes.append(Volume(v_index, chapter.start_paragraph_index - 1, v_paragraph, None))
                v_chars = 0
                v_index = chapter.start_paragraph_index
                v_paragraph = None
            elif v_chars + chapter.chars > self.max_chars_per_volume:
                middle_paragraph_index, chars_left_in_chapter = self.split_chapter(chapter.start_paragraph_index,
                                                                                   chapter.end_paragraph_index,
                                                                                   v_chars + chapter.chars,
                                                                                   self.max_chars_per_volume)
                if middle_paragraph_index != chapter.end_paragraph_index:
                    self.volumes.append(Volume(v_index, middle_paragraph_index, v_paragraph, SPLIT_CHAPTER_END))
                    self.chapters.insert(c_index + 1,
                                         Chapter(chars_left_in_chapter, middle_paragraph_index + 1, chapter.end_paragraph_index))
                    self.chapters[c_index].end_paragraph_index = middle_paragraph_index
                    self.chapters[c_index].chars = v_chars + chapter.chars - chars_left_in_chapter
                    v_index = middle_paragraph_index + 1
                    v_paragraph = SPLIT_CHAPTER_START.format(c_index)
                else:
                    self.volumes.append(Volume(v_index, middle_paragraph_index, v_paragraph, None))
                v_chars = 0
                c_index += 1
            elif v_chars + chapter.chars > self.min_chars_per_volume:
                self.volumes.append(Volume(v_index, chapter.end_paragraph_index, v_paragraph, None))
                v_chars = 0
                v_index = chapter.end_paragraph_index + 1
                v_paragraph = None
                c_index += 1
            else:
                v_chars += chapter.chars
                c_index += 1

        logging.info("book will be split into {} volumes".format(len(self.volumes)))

    # todo אריה במדבר במקום
    def split_chapter(self, first_index, last_index, chars, max_chars):
        current_chars_count = chars
        chars_left_in_chapter = 0
        while current_chars_count > max_chars and last_index > first_index:
            chars_in_paragraph = len(self.paragraphs[last_index].text)
            current_chars_count = current_chars_count - chars_in_paragraph
            last_index -= 1
            chars_left_in_chapter += chars_in_paragraph
        return last_index, chars_left_in_chapter
