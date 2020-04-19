from general.book import *
import os
from docx import Document
from general.constants import *
from docx.enum.style import WD_STYLE_TYPE
import logging


def start_split(input_path, gui_queue):
    create_split(input_path)
    gui_queue.put("split")
    return


def start_stickers(directory, title, author, volumes, pages, gui_queue):
    create_stickers(directory, title, author, volumes, pages)
    gui_queue.put("stickers")
    return

# todo
#  handle exception gracefully!!!!
# check if we really need \כויות יוצרים בכל כרך?
def create_split(path):
    logging.debug("start split {} to volumes")

    origin = Document(path)

    directory = os.path.splitext(path)[0]
    try:
        os.mkdir(directory)
        logging.info("created a directory at {}".format(directory))
    except FileExistsError:
        logging.warning("directory {} already exists".format(directory))
        pass

    book = Book(origin.paragraphs)
    volumes = book.volumes

    volumes_count = len(volumes)

    for index, vol in enumerate(volumes, 1):
        vol.create_doc(path, book.last_gate_paragraph, index, volumes_count)
        volume_path = "{dir}/{vol}.{docx}".format(dir=directory, vol=str(index), docx=DOCX)
        vol.doc.save(volume_path)

    logging.debug("done split to volume, all saved in the file system")


def create_stickers(directory, book_title, book_author, num_volumes, num_pages):
    logging.debug("start creating stickers")

    doc = Document(TEMPLATE)
    style = doc.styles.add_style(STICKER, WD_STYLE_TYPE.PARAGRAPH)
    style.paragraph_format.keep_together = True

    sticker_template = NORMAL_STICKER_TEMPLATE
    if num_pages.strip() != '':
        sticker_template = STUDY_STICKER_TEMPLATE

    for i in range(int(num_volumes)):
        sticker = sticker_template.format(title=book_title,
                                          author=book_author,
                                          total=VOLUMES_NAMES_2[int(num_volumes)-1],
                                          current=VOLUMES_NAMES_1[i],
                                          pages=num_pages)
        doc.add_paragraph(text=sticker, style=style)
    path = "{dir}/{sticker}.{docx}".format(dir=directory, sticker=STICKER, docx=DOCX)

    doc.save(path)

    logging.debug("done creating stickers, output saved at {}".format(path))
