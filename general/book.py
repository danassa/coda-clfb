from general.constants import *
import logging
from general.volume import Volume
from general.chapter import Chapter
import math


class Book:

    def __init__(self, elements, min_chars=MIN_CHARS_PER_VOLUME, max_chars=MAX_CHARS_PER_VOLUME):
        logging.info("book initialization began. a volume will contain {} to {} characters".format(min_chars, max_chars))
        assert min_chars <= max_chars, "minimum characters per volume must be equal or greater than the maximum"

        self.elements = elements
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
        for index, element in enumerate(self.elements):
            if GATE_END_INDICATOR in element.block.text:
                self.last_gate_paragraph = index + 1
                return
        logging.error("no copyright paragraph found! cannot distinguish between gate pages and the rest of the content")

    def create_chapters(self):
        total_chars = 0
        chapter_chars = 0
        current_chapter_start_index = self.last_gate_paragraph

        for index, element in enumerate(self.elements):
            if element.is_paragraph and element.block.text == CHAPTER_INDICATOR:
                if current_chapter_start_index != self.last_gate_paragraph:
                    new_chapter = Chapter(chapter_chars, current_chapter_start_index, index - 1)
                    self.chapters.append(new_chapter)
                    total_chars += chapter_chars
                    chapter_chars = 0
                current_chapter_start_index = index + 1
            elif index >= self.last_gate_paragraph:
                chapter_chars += element.chars_count()

        total_chars += chapter_chars
        last_chapter = Chapter(chapter_chars, current_chapter_start_index, len(self.elements)-1)
        self.chapters.append(last_chapter)
        self.chars = total_chars
        logging.info("Found {} actual chapters in the book, with a total of {} characters"
                     .format(len(self.chapters), self.chars))

        # for i, c in enumerate(self.chapters):
        #     logging.debug("\nchapter " + str(i) + ": " + str(c.start_index) + " - " + str(c.end_index) + ": '" +
        #                  self.paragraphs[c.start_index].text + "' - '" + self.paragraphs[c.end_index].text)

    def split_volumes(self):
        c_index = 0
        v_chars = 0
        v_index = self.last_gate_paragraph + 1
        v_paragraph = None
        fst_c_index_in_v = 0
        lst_c_index_in_v = 0

        while True:
            try:
                chapter = self.chapters[c_index]
            except IndexError:
                if v_chars > 0:
                    self.volumes.append(Volume(chars=v_chars,
                                               start=v_index,
                                               end=self.chapters[c_index-1].end_index,
                                               fst_c_index_in_v=fst_c_index_in_v,
                                               lst_c_index_in_v=lst_c_index_in_v,
                                               first_paragraph=v_paragraph))
                break

            if v_chars + chapter.chars > self.max_chars_per_volume and v_chars > self.min_chars_per_volume:
                self.volumes.append(Volume(chars=v_chars,
                                           start=v_index,
                                           end=chapter.start_index - 1,
                                           fst_c_index_in_v=fst_c_index_in_v,
                                           lst_c_index_in_v=lst_c_index_in_v,
                                           first_paragraph=v_paragraph))
                v_chars = 0
                v_index = chapter.start_index
                fst_c_index_in_v = lst_c_index_in_v = c_index
                v_paragraph = None
            elif v_chars + chapter.chars > self.max_chars_per_volume:
                middle_index, chars_left_in_chapter = self.split_chapter(chapter.start_index,
                                                                                   chapter.end_index,
                                                                                   v_chars + chapter.chars,
                                                                                   self.max_chars_per_volume)
                v_chars = v_chars + chapter.chars - chars_left_in_chapter
                if middle_index != chapter.end_index:
                    self.volumes.append(Volume(chars=v_chars,
                                               start=v_index,
                                               end=middle_index,
                                               fst_c_index_in_v=fst_c_index_in_v,
                                               lst_c_index_in_v=c_index,
                                               first_paragraph=v_paragraph,
                                               last_paragraph=SPLIT_CHAPTER_END))
                    self.chapters.insert(c_index + 1,
                                         Chapter(chars_left_in_chapter, middle_index + 1, chapter.end_index))
                    self.chapters[c_index].end_index = middle_index
                    self.chapters[c_index].chars = chapter.chars - chars_left_in_chapter
                    v_index = middle_index + 1
                    v_paragraph = SPLIT_CHAPTER_START.format(c_index)
                else:
                    self.volumes.append(Volume(chars=v_chars,
                                               start=v_index,
                                               end=middle_index,
                                               fst_c_index_in_v=fst_c_index_in_v,
                                               lst_c_index_in_v=c_index,
                                               first_paragraph=v_paragraph))
                fst_c_index_in_v = lst_c_index_in_v = c_index + 1
                v_chars = 0
                c_index += 1
            elif v_chars + chapter.chars > self.min_chars_per_volume:
                self.volumes.append(Volume(chars=v_chars + chapter.chars,
                                           start=v_index,
                                           end=chapter.end_index,
                                           fst_c_index_in_v=fst_c_index_in_v,
                                           lst_c_index_in_v=c_index,
                                           last_paragraph=v_paragraph))
                fst_c_index_in_v = lst_c_index_in_v = c_index + 1
                v_chars = 0
                v_index = chapter.end_index + 1
                v_paragraph = None
                c_index += 1
            else:
                lst_c_index_in_v = c_index
                v_chars += chapter.chars
                c_index += 1

        self.fix_too_short_last_volume()

        logging.info("book will be split into {} volumes".format(len(self.volumes)))

        # for i, v in enumerate(self.volumes):
        #     logging.debug("volume " + str(i) + "- chapters: " + str(v.first_chapter_index)+ " - " + str(v.last_chapter_index)
        #                  + ", paragraphs: " + str(v.start_index) + " - " + str(v.end_index) + ": '" +
        #                  self.paragraphs[v.start_index].text + "' - '" + self.paragraphs[v.end_index].text)

    def split_chapter(self, first_index, last_index, chars, max_chars):
        current_chars_count = chars
        chars_left_in_chapter = 0
        while current_chars_count > max_chars and last_index > first_index:
            chars_in_element = self.elements[last_index].chars_count()
            current_chars_count = current_chars_count - chars_in_element
            last_index -= 1
            chars_left_in_chapter += chars_in_element
        return last_index, chars_left_in_chapter

    def fix_too_short_last_volume(self):
        num_volumes = len(self.volumes)
        if self.volumes[-1].chars < self.calc_min_chars_per_last_volume():
            last_volume = self.volumes[num_volumes - 1]
            before_last_volume = self.volumes[num_volumes - 2]
            chapters_in_last_volume = last_volume.last_chapter_index - last_volume.first_chapter_index
            chapters_in_before_last_volume = before_last_volume.last_chapter_index - before_last_volume.first_chapter_index
            chapters_to_move = math.floor((chapters_in_before_last_volume - chapters_in_last_volume) / 2)
            if chapters_to_move >= 1:
                chars_to_move = 0
                new_first_chapter_in_last_volume = last_volume.first_chapter_index - chapters_to_move
                new_last_paragraph_in_last_volume = self.chapters[new_first_chapter_in_last_volume].start_index
                for index in range(new_first_chapter_in_last_volume, last_volume.first_chapter_index):
                    chars_to_move += self.elements[index].chars_count()
                last_volume.update_first_chapter(chars_to_move, new_last_paragraph_in_last_volume)
                before_last_volume.update_last_chapter(chapters_to_move, new_last_paragraph_in_last_volume - 1)

    def calc_min_chars_per_last_volume(self):
        return round(2 / 3 * self.min_chars_per_volume)
