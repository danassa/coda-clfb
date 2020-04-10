import queue
import threading
import PySimpleGUI as sg
from constants import *
from split import generate_outputs
from book import get_now, get_elapsed_time_str
from sticker import create_stickers
# todo logs!


def the_gui():
    sg.theme('BlueMono')
    layout = [
        [sg.Frame(title='המרת ספר לכרכים',
                  pad=((5, 5), (10, 10)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_PATH, enable_events=True, justification='r', size=(80, 1)),
                       sg.FileBrowse(button_text="בחר ספר", size=(11, 1))],
                      [sg.Text('00:00', key=G_TIMER),
                       sg.Button(G_SPLIT), sg.Text('', size=(20, 1))],
                      [sg.Text('')]
                  ]
                  )],

        [sg.Frame(title='יצירת מדבקות',
                  pad=((5, 5), (10, 10)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_TITLE, size=(40, 1), enable_events=True),
                       sg.Text('כותר:', size=(11, 1), justification='r')],
                      [sg.Input(key=G_AUTHOR, size=(40, 1)),
                       sg.Text('מחבר:', size=(11, 1), justification='r')],
                      [sg.Input(key=G_VOLUMES, size=(5, 1)),
                       sg.Text('מספר כרכים:', size=(11, 1), justification='r')],
                      [sg.Input(key=G_PAGES, size=(5, 1)),
                       sg.Text('ספר לימוד? אם כן, הזן מספר עמודים:')],
                      [sg.Input(key=G_DIR, enable_events=True, justification='r', size=(80, 1)),
                       sg.FolderBrowse(button_text="בחר תיקייה", size=(11, 1))],
                      [sg.Button(G_STICKER), sg.Text('', size=(20, 1))],
                      [sg.Text('')]
                  ]
                  )],
        [sg.Button(G_EXIT)],
        [sg.Text('')]
    ]

    window = sg.Window(G_WINDOW_TITLE, layout, finalize=True)
    gui_queue = queue.Queue()

    start_time = 0

    while True:
        event, values = window.Read(timeout=100)

        if event is None or event == G_EXIT:
            break

        if event == G_SPLIT:
            if values[G_PATH] == '':
                sg.popup("You MUST pick a file!", title='')
            else:
                start_time = get_now()
                window[G_SPLIT].Update(disabled=True)
                window[G_STICKER].Update(disabled=True)
                thread_id = threading.Thread(target=start_split, args=(values[G_PATH], gui_queue), daemon=True)
                thread_id.start()

        if event == G_STICKER:
            error = validate_sticker_inputs(values)
            if error is not None:
                sg.popup(error, title='שגיאה', line_width=100)
            else:
                thread_id = threading.Thread(target=start_stickers, args=(
                    values[G_DIR], values[G_TITLE], values[G_AUTHOR], values[G_VOLUMES], values[G_PAGES], gui_queue
                ), daemon=True)
                thread_id.start()

        try:
            gui_queue.get_nowait()
            sg.popup("Done!")
            start_time = 0
            window[G_SPLIT].Update(disabled=False)
            window[G_STICKER].Update(disabled=False)
        except queue.Empty:
            pass

        if start_time != 0:
            window[G_TIMER].Update(value=get_elapsed_time_str(start_time))

    window.Close()


def start_split(input_path, gui_queue):
    generate_outputs(input_path)
    gui_queue.put("split")
    return


def start_stickers(directory, title, author, volumes, pages, gui_queue):
    create_stickers(directory, title, author, volumes, pages)
    gui_queue.put("stickers")
    return


def validate_sticker_inputs(values):
    if values[G_TITLE].strip() == '' or \
            values[G_AUTHOR].strip() == '':
        return "אנא וודא שהזנת כותר ומחבר!"
    if not values[G_VOLUMES].isdigit() or \
            int(values[G_VOLUMES]) > 30 or \
            int(values[G_VOLUMES]) < 1:
        return "אנא הזן מספר תקני של כרכים (בין 1 ל-30)!"
    if values[G_PAGES].strip() != '' and \
            not values[G_PAGES].isdigit():
        return "אנא בדוק את מספר העמודים שהזנת!"
    if values[G_DIR].strip() == '':
        return "אנא בחר תיקייה בה יישמר הפלט"

    return None


the_gui()
