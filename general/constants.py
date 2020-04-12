import time

LOG_FILE = "coda.log"

MAX_CHARS_PER_VOLUME = 5000
MIN_CHARS_PER_VOLUME = 2000

# resource file containing default settings for output documents (Ariel font, size 14, Right-To-Left)
TEMPLATE = 'template.docx'

# this magic string should be added before each new chapter by the person editing the doc prior to it being
# submitted to this program. this will allow us to distinguish between chapters, since normally there is no
# consistency between different books.
MAGIC_STRING = 'תחילת פרק חדש - קודה'

GATE_END_INDICATOR = "העתקה או העברה של העותק"
CHAPTER_INDICATOR = "תחילת פרק חדש"

SPLIT_CHAPTER_END = "המשך הפרק בכרך הבא"
SPLIT_CHAPTER_START = "המשך פרק {}"

FIRST_PAGE_VOLUMES_PARAGRAPH = "כרך ראשון"

DOCX = 'docx'
BOOK_SUFFIX = 'סוף הספר'
END = 'סוף '

G_TIMER = 'Timer'
G_PATH = 'Path'
G_SPLIT = 'חלק לכרכים!'
G_STICKER = 'צור מדבקות!'
G_EXIT = 'סגור'
G_HELP = 'תמיכה'

G_TITLE = 'Title'
G_AUTHOR = 'Author'
G_VOLUMES = 'Volumes'
G_PAGES = 'Pages'
G_WINDOW_TITLE = 'Coda; הספריה המרכזית לעיוורים ובעלי לקויות קריאה'
G_DIR = 'Directory'

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
עמודים {pages}
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


def get_now():
    return int(round(time.time() * 100))


def get_elapsed_time_str(start_time):
    elapsed_time = get_now() - start_time
    display_time = '{:02d}:{:02d}'.format((elapsed_time // 100) // 60, (elapsed_time // 100) % 60)
    return display_time
