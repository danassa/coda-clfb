import time

LOG_FILE = "log.txt"
CONF_FILE = "config.ini"

MAX_CHARS_PER_VOLUME = 65000
MIN_CHARS_PER_VOLUME = 55000


# this magic string should be added before each new chapter by the person editing the doc prior to it being
# submitted to this program. this will allow us to distinguish between chapters, since normally there is no
# consistency between different books.
CHAPTER_INDICATOR = "תחילת פרק חדש"

GATE_END_INDICATOR = "העתקה או העברה של העותק"

SPLIT_CHAPTER_END = "המשך הפרק בכרך הבא"
SPLIT_CHAPTER_START = "המשך פרק {}"

FIRST_PAGE_VOLUMES_PARAGRAPH = "כרך ראשון"

DOCX = 'docx'
DOC = 'doc'
BOOK_SUFFIX = 'סוף הספר'
END = 'סוף '

G_TIMER = 'Timer'
G_PATH = 'Path'
G_SPLIT = 'חלק לכרכים'
G_STICKER = 'צור מדבקות'
G_EXIT = 'סגור'
G_HELP = 'תמיכה'
G_PICK_BOOK = 'בחר ספר'
G_TITLE = 'כותר'
G_AUTHOR = 'מחבר'
G_VOLUMES = 'מספר כרכים'
G_PAGES = 'עמודים'
G_PICK_DIR = 'בחר תיקייה'
G_DIR = 'Directory'
G_WINDOW_TITLE = 'הכנת ספרים להמרה לכתב ברייל'

STICKER = 'מדבקה'

NORMAL_STICKER_TEMPLATE = """
הספריה המרכזית לעיוורים
{title}
מאת: {author}
{total} - {current}


"""

STUDY_STICKER_TEMPLATE = """
הספריה המרכזית לעיוורים
{title}
מאת: {author}
{total} - {current}
{pages} עמודים
הספר לא להחזרה


"""

VOLUMES_NAMES_1 = [
    'כרך ראשון',
    'כרך שני',
    'כרך שלישי',
    'כרך רביעי',
    'כרך חמישי',
    'כרך שישי',
    'כרך שביעי',
    'כרך שמיני',
    'כרך תשיעי',
    'כרך עשירי',
    'כרך אחד-עשר',
    'כרך שנים-שער',
    'כרך שלושה-עשר',
    'כרך ארבעה-עשר',
    'כרך חמישה-עשר',
    'כרך שישה-עשר',
    'כרך שבעה-עשר',
    'כרך שמונה-עשר',
    'כרך תשעה-עשר',
    'כרך עשרים',
    'כרך עשרים ואחד',
    'כרך עשרים ושניים',
    'כרך עשרים ושלושה',
    'כרך עשרים וארבעה',
    'כרך עשרים וחמישה',
    'כרך עשרים ושישה',
    'כרך עשרים ושבעה',
    'כרך עשרים ושמונה',
    'כרך עשרים ותשעה',
    'כרך שלושים'
]

VOLUMES_NAMES_2 = [
    'בכרך אחד',
    'בשני כרכים',
    'בשלושה כרכים',
    'בארבעה כרכים',
    'בחמישה כרכים',
    'בשישה כרכים',
    'בשבעה כרכים',
    'בשמונה כרכים',
    'בתשעה כרכים',
    'בעשרה כרכים',
    'באחד-עשר כרכים',
    'בשנים-עשר כרכים',
    'בשלושה-עשר כרכים',
    'בארבעה-עשר כרכים',
    'בחמישה-עשר כרכים',
    'בשישה-עשר כרכים',
    'בשבעה-עשר כרכים',
    'בשמונה-עשר כרכים',
    'בתשעה-עשר כרכים',
    'בעשרים כרכים',
    'בעשרים ואחד כרכים',
    'בעשרים ושניים כרכים',
    'בעשרים ושלושה כרכים',
    'בעשרים וארבעה כרכים',
    'בעשרים וחמישה כרכים',
    'בעשרים ושישה כרכים',
    'בעשרים ושבעה כרכים',
    'בעשרים ושמונה כרכים',
    'בעשרים ותשעה כרכים',
    'בשלושים כרכים'
]

F0 = ("Ariel", 14)
F1 = ("Ariel", 11)

SUCCESS = True
FAILURE = not SUCCESS

ERROR_MESSAGE = """{}
        
אפשר לבדוק בקובץ log.txt את פרטי השגיאה
"""

ERROR_TITLE = "ארעה שגיאה"


def get_now():
    return int(round(time.time() * 100))


def get_elapsed_time_str(start_time):
    elapsed_time = get_now() - start_time
    display_time = '{:02d}:{:02d}'.format((elapsed_time // 100) // 60, (elapsed_time // 100) % 60)
    return display_time
