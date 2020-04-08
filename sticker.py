from docx import Document
from constants import *
from docx.enum.style import WD_STYLE_TYPE


def create_stickers(directory, book_title, book_author, num_volumes, num_pages):
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