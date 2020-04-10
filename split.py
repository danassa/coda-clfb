from book import *
import os
from constants import *


def generate_outputs(path):
    origin = Document(path)

    directory = os.path.splitext(path)[0]
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass

    book = Book(origin.paragraphs)
    volumes = book.volumes

    volumes_count = len(volumes)

    for index, vol in enumerate(volumes):
        vol.create_doc(path, book.last_gate_paragraph, index, volumes_count)
        volume_path = "{dir}/{vol}.{docx}".format(dir=directory, vol=str(index + 1), docx=DOCX)
        vol.doc.save(volume_path)
