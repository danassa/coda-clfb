import queue
import threading
import PySimpleGUI as sg
from general.constants import *
from general.logic import start_stickers, start_split
import logging


def create_gui(max_chars, min_chars):
    logging.info('Initializing GUI..')
    sg.theme('BlueMono')
    layout = [
        [sg.Frame(title='המרת ספר לכרכים',
                  pad=((5, 5), (12, 12)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  font=F0,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_PATH, enable_events=True, font=F1, size=(60, 1)),
                       sg.FileBrowse(button_text=G_PICK_BOOK, key=G_PICK_BOOK, font=F1, size=(10, 1))],
                      [sg.Button(G_SPLIT, font=F1, size=(15, 1)),
                       sg.Text('00:00', font=F1, key=G_TIMER),
                       sg.Text('', size=(57, 1))],
                      [sg.Text('')]
                  ]
                  )],

        [sg.Frame(title='יצירת מדבקות',
                  pad=((5, 5), (12, 12)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  font=F0,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_TITLE, size=(40, 1), enable_events=True, justification='r', font=F1),
                       sg.Text(G_TITLE, size=(11, 1), justification='r', font=F1)],
                      [sg.Input(key=G_AUTHOR, size=(40, 1), justification='r', font=F1),
                       sg.Text(G_AUTHOR, size=(11, 1), justification='r', font=F1)],
                      [sg.Input(key=G_VOLUMES, size=(5, 1), justification='r', font=F1),
                       sg.Text(G_VOLUMES, size=(11, 1), justification='r', font=F1)],
                      [sg.Input(key=G_PAGES, size=(5, 1), justification='r', font=F1),
                       sg.Text('ספר לימוד? אם כן, הזן מספר עמודים:', justification='r', font=F1)],
                      [sg.Input(key=G_DIR, enable_events=True, size=(60, 1), font=F1),
                       sg.FolderBrowse(button_text=G_PICK_DIR, key=G_PICK_DIR, size=(10, 1), font=F1)],
                      [sg.Button(G_STICKER, font=F1, size=(15, 1)), sg.Text('', size=(64, 1))],
                      [sg.Text('')]
                  ]
                  )],
        [sg.Button(G_EXIT, font=F1, size=(15, 1)), sg.Button(G_HELP, font=F1, size=(15, 1))],
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
                toggle_buttons(window, True)
                thread_id = threading.Thread(target=start_split, daemon=True,
                                             args=(values[G_PATH], gui_queue, max_chars, min_chars))
                thread_id.start()

        if event == G_STICKER:
            error = validate_sticker_inputs(values)
            if error is not None:
                sg.popup(ERROR_MESSAGE.format(error), title=ERROR_TITLE, line_width=100)
            else:
                start_time = get_now()
                thread_id = threading.Thread(target=start_stickers, daemon=True,
                                             args=(values[G_DIR], values[G_TITLE], values[G_AUTHOR],
                                                   values[G_VOLUMES], values[G_PAGES], gui_queue))
                thread_id.start()

        try:
            response = gui_queue.get_nowait()
            logging.info("done with status {} - {}, time elapsed: {}".format(response[0], response[1], get_elapsed_time_str(start_time)))
            if response[0] == SUCCESS:
                sg.popup("הפעולה הושלמה בהצלחה. מיקום המסמכים:\n\n" + response[1])
            else:
                sg.popup(response[1], title=ERROR_TITLE)
            start_time = 0
            toggle_buttons(window, False)
        except queue.Empty:
            pass

        if start_time != 0:
            window[G_TIMER].Update(value=get_elapsed_time_str(start_time))

    window.Close()


def validate_sticker_inputs(values):
    if values[G_TITLE].strip() == '' or \
            values[G_AUTHOR].strip() == '':
        logging.error("validation of user inputs for sticker creation failed: title must not be empty: '{}', "
                      "author must not be empty: '{}'".format(values[G_TITLE], values[G_AUTHOR]))
        return "אנא וודא שהזנת כותר ומחבר!"
    if not values[G_VOLUMES].isdigit() or \
            int(values[G_VOLUMES]) > 30 or \
            int(values[G_VOLUMES]) < 1:
        logging.error("validation of user inputs for sticker creation failed: volumes should be "
                      "between 1 to 30: '{}'".format(values[G_VOLUMES]))
        return "אנא הזן מספר תקני של כרכים (בין 1 ל-30)!"
    if values[G_PAGES].strip() != '' and \
            not values[G_PAGES].isdigit():
        logging.error("validation of user inputs for sticker creation failed: pages are not a number: '{}'".format(values[G_PAGES]))
        return "אנא בדוק את מספר העמודים שהזנת!"
    if values[G_DIR].strip() == '':
        logging.error("validation of user inputs for sticker creation failed: no directory was selected for output.")
        return "אנא בחר תיקייה בה יישמר הפלט"

    return None


def toggle_buttons(window, disabled):
    window[G_SPLIT].Update(disabled=disabled)
    window[G_PICK_BOOK].Update(disabled=disabled)
    window[G_STICKER].Update(disabled=disabled)
    window[G_PICK_DIR].Update(disabled=disabled)

