import logging


class Chapter:
    def __init__(self, chars, start, end):
        """
        :param chars: total count of characters in all this chapter's paragraphs
        :param start: index of the book's paragraphs which is the FIRST in this chapter
        :param end: index of the book's paragraphs which is be the FIRST in this chapter
        """
        assert end >= start
        assert chars > 0
        self.chars = chars
        self.start_paragraph_index = start
        self.end_paragraph_index = end
        logging.debug("Chapter created with {}, paragraphs: {} to {}"
                      .format(self.chars, self.start_paragraph_index, self.end_paragraph_index))
