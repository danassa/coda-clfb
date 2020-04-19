from general.book import *
import os
from docx import Document
from general.constants import *
from docx.enum.style import WD_STYLE_TYPE
import logging
from copy import deepcopy
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from general.element import Element
from general.generator import DocxGenerator


def start_split(input_path, gui_queue):
    try:
        create_split(input_path)
        gui_queue.put("Done Split to Volumes")
    except Exception as error:
        error_type = type(error)
        logging.error(error_type)
        logging.exception(error)
        gui_queue.put("Failed Split. {} error occurred - {}. Check the logs!".format(error_type, error))
    return


def start_stickers(directory, title, author, volumes, pages, gui_queue):
    create_stickers(directory, title, author, volumes, pages)
    gui_queue.put("Done Creating Stickers")
    return


def create_split(path):
    logging.info("start split {} to volumes")

    origin = Document(path)

    directory = os.path.splitext(path)[0]
    try:
        os.mkdir(directory)
        logging.info("created a directory at {}".format(directory))
    except FileExistsError:
        logging.warning("directory {} already exists".format(directory))
        pass

    book = Book(build_elements_list(origin))
    font = origin.paragraphs[book.last_gate_paragraph - 1].runs[-1].font
    volumes = book.volumes
    volumes_count = len(volumes)

    # for index, vol in enumerate(volumes, 1):
    #     new_doc = deepcopy(origin)
    #     elements = build_elements_list(new_doc)
    #
    #     g = DocxGenerator(new_doc, elements, book.last_gate_paragraph, vol, index, volumes_count, font)
    #     g.format_volume()
    #     g.save(directory)

    for index, vol in enumerate(volumes, 1):
        new_doc = deepcopy(origin)
        elements = build_elements_list(new_doc)
        vol.create_doc(new_doc, elements, book.last_gate_paragraph, index, volumes_count)
        volume_path = "{dir}/{vol}.{docx}".format(dir=directory, vol=str(index), docx=DOCX)
        new_doc.save(volume_path)


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


def build_elements_list(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    elements = []
    for index, child in enumerate(parent_elm.iterchildren()):
        if isinstance(child, CT_P):
            elements.append(Element(True, Paragraph(child, parent)))
        elif isinstance(child, CT_Tbl):
            elements.append(Element(False, Table(child, parent)))
    return elements
