# coda-clfb
Automatization tool for the central library for the blind, IL


לוודא עם אסתי אם לעבוד לפי תווים!!

OS - Windows 10
Conversion Program - Duxbury

doc vs docx:
input file can be .docx, output file must be .doc :
the program that process the output into Braille is ignoring some formatting of the document when a .docx is submitted
(Esti mentioned the headers goes missing).

stickers:
The stickers they are requesting should be generated independently from the split output.
This is becuase the stickers contian number of pages, which they know only after the book was converted into Braille.

chapters:
chapter will look different for each book. we agreed it would be best to mark the start of a new chapter somehow by the
person who is editing the book prior to it being submitted to this program. so we will determine some magic string
and will implement according to that.



Requirements:

כדי לראות שאפשר לכתוב את הכלי אז השלב הראשון הוא לכתוב כלי שמקבל קובץ וורד ומפצל אותו לקבצי וורד שבכל אחד מהם 20 עמודים.
כאשר הכלי הזה יפעל אז אפשר יהיה להתקדם לכלי שהספרייה מבקשת:
1.     גופן המסמך יהיה – arial 14
2.     כל כרך יהיה בין 25-30 עמודים תלוי בעומס מלל בטקסט. אם אפשר לזהות את הפרק אז להשתדל לא לפצל באמצע פרק.
3.     בסוף כל כרך לרשום – סוף כרך ראשון, שני, שלישי וכו'
4.     אם הכרך לא מסתיים בסוף הפרק, יש לרשום הערה בסוגריים (המשך הפרק בכרך הבא) ובתחילת כרך הבא לרשום הערה בסוגריים לדוגמה (המשך פרק 5: אמא)
5.     בסוף הספר רושמים – סוף הספר
6.     לכל שער מחברים את השער ומשנים את הפרטים כמו: מספר הכרך, מספרי עמודי ברייל ובספרי לימוד מספרי דפוס.(אם הספר כתוב בניקוד חלקי, יש להוסיף את הניקוד גם בשער - פרטים שאנחנו מכניסים)
7.     מכינים מדבקה לכל הכרכים:
הכיתוב במדבקה
הספריה המרכזית לעיוורים
שם הספר
שם הסופר
בכמה כרכים – כרך ראשון, שני, שלישי וכו'
עמודי דפוס (אם זה ספר לימוד)
הספר לא להחזרה (אם זה ספר לימוד)



Several issues:

word documents do not have "pages" per say. text is not linked to a specific page. It is linked to paragraph entities,
but you cannot count pages in the way the requirements intended (unless you do some calculations considering font and page dimensions).

doc format is very outdated. there are almost no libraries handling this format, better use docx format.
when trying to convert programmatically, you are depended on the OS.

C# is probably best for this project requirements. The free libraries in python and java are not very impressive.
There are some better libraries, but they require license.
Unfortunately, I have no idea how to use C# and I am not keen on learning it.



Libraries to install (pip install...):

- python-docx	0.8.10
- PySimpleGUI	4.18.0
- pyinstaller


Create app for Windows end user:

- Copy this project to a Windows OS
- Install Python3 (if missing) and the libraries mentioned above
- run the below command from within the /coda directory
pyinstaller --onefile -wF --add-data 'template.docx;.' gui.py

This will create a 'dist' folder containing an .exe file you can distribute to the end-user.