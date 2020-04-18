import queue
import threading
import PySimpleGUI as sg
from general.constants import *
from general.logic import start_stickers, start_split
import logging


logFormatter = logging.Formatter("%(asctime)s %(levelname)s:%(funcName)s %(message)s")
fileHandler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
fileHandler.setFormatter(logFormatter)
streamHandler = logging.StreamHandler()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logging.info('Starting C.L.F.B Tool..')


f1 = ("Ariel", 11)
f0 = ("Ariel", 14)


def the_gui():
    logging.info('Initializing GUI..')
    sg.theme('BlueMono')
    layout = [
        [sg.Frame(title='המרת ספר לכרכים',
                  pad=((5, 5), (12, 12)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  font=f0,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_PATH, enable_events=True, justification='r', font=f1, size=(60, 1)),
                       sg.FileBrowse(button_text="בחר ספר", font=f1, size=(10, 1))],
                      [sg.Button(G_SPLIT, font=f1, size=(15, 1)),
                       sg.Text('00:00', font=f1, key=G_TIMER),
                       sg.Text('', size=(57, 1))],
                      [sg.Text('')]
                  ]
                  )],

        [sg.Frame(title='יצירת מדבקות',
                  pad=((5, 5), (12, 12)),
                  title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                  element_justification="r",
                  relief=sg.RELIEF_GROOVE,
                  font=f0,
                  layout=[
                      [sg.Text('')],
                      [sg.Input(key=G_TITLE, size=(40, 1), enable_events=True, font=f1),
                       sg.Text('כותר:', size=(11, 1), justification='r', font=f1)],
                      [sg.Input(key=G_AUTHOR, size=(40, 1), font=f1),
                       sg.Text('מחבר:', size=(11, 1), justification='r', font=f1)],
                      [sg.Input(key=G_VOLUMES, size=(5, 1), font=f1),
                       sg.Text('מספר כרכים:', size=(11, 1), justification='r', font=f1)],
                      [sg.Input(key=G_PAGES, size=(5, 1), font=f1),
                       sg.Text('ספר לימוד? אם כן, הזן מספר עמודים:', font=f1)],
                      [sg.Input(key=G_DIR, enable_events=True, justification='r', size=(60, 1), font=f1),
                       sg.FolderBrowse(button_text="בחר תיקייה", size=(10, 1), font=f1)],
                      [sg.Button(G_STICKER, font=f1, size=(15, 1)), sg.Text('', size=(64, 1))],
                      [sg.Text('')]
                  ]
                  )],
        [sg.Button(G_EXIT, font=f1, size=(15, 1)), sg.Button(G_HELP, font=f1, size=(15, 1))],
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
                start_time = get_now()
                thread_id = threading.Thread(target=start_stickers, args=(
                    values[G_DIR], values[G_TITLE], values[G_AUTHOR], values[G_VOLUMES], values[G_PAGES], gui_queue
                ), daemon=True)
                thread_id.start()

        try:
            message = gui_queue.get_nowait()
            logging.info("done with task {}, time elapsed: {}".format(message, get_elapsed_time_str(start_time)))
            sg.popup("Done!")
            start_time = 0
            window[G_SPLIT].Update(disabled=False)
            window[G_STICKER].Update(disabled=False)
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


the_gui()
