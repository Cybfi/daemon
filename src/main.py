# GLOBALS
from lib.GlobalManager import gmget, gmset
from lib.RuntimeReporter import RuntimeReporter
from lib.SimpleLogger import SimpleLogger
from lib.WordList import WordList

_LOGGER: SimpleLogger = gmset("logger", SimpleLogger("Cyber"))
_RTMAN:  RuntimeReporter = gmset("reporter", RuntimeReporter())
_BWLIST: WordList = gmset("bwlist", WordList("https://dl.cybfi.net/badwordlist"))

from os import getenv
AppData = getenv('HOMEDRIVE') + getenv('HOMEPATH') + "\\AppData\\Local"

# DEPRECATED: in favour of lib.WordList:WordList
def download_word_list():
    from pathlib import Path
    from requests import get
    from os import mkdir

    try:
        open(AppData + "\\Cyber\\badwordlist", "w").close()
    except FileNotFoundError:
        mkdir(AppData + "\\Cyber")
        open(AppData + "\\Cyber\\badwordlist", "w").close()

    filename = Path(AppData + "\\Cyber\\badwordlist")
    filename.write_bytes(get("https://dl.cybfi.net/badwordlist", allow_redirects=True).content)


def check_text(input):
    from os import path
    from time import time

    # if bwlist is older than 15 minutes, fetch
    if _BWLIST.decayed_fetch(1000):
        gmset("bwlist", _BWLIST)

    if _BWLIST.check(input):
        return True
    return False

def keylogging():
    # Import dependencies
    from keyboard import on_press, wait

    class Keylogger:
        def __init__(self):
            self.line_typed = ""

        def callback(self, event):
            name = event.name

            if len(name) != 1:
                if name == "space":
                    name = " "
                elif name == "decimal":
                    name = "."
                elif name == "enter":
                    name = ""
                    if check_text(self.line_typed):
                        print("Problem detected! Reporting...")

                self.line_typed += name
            else:
                self.line_typed += name

        def start(self):
            # When key pressed
            while True:
                on_press(callback=self.callback)
                wait()

    m = Keylogger()
    m.start()


# Capture the screen
def analyze_screen():
    # noinspection PyUnresolvedReferences
    from cv2 import COLOR_BGR2GRAY, cvtColor, threshold, THRESH_OTSU, THRESH_BINARY_INV, \
        getStructuringElement, MORPH_RECT, dilate, findContours, RETR_EXTERNAL, \
        CHAIN_APPROX_NONE, boundingRect

    from pyautogui import screenshot
    from pytesseract import pytesseract
    from numpy import array
    from time import sleep

    def read_screen():
        pytesseract.tesseract_cmd = './tesseract/tesseract.exe'
        img = array(screenshot())
        gray = cvtColor(img, COLOR_BGR2GRAY)
        ret, thresh1 = threshold(gray, 0, 255, THRESH_OTSU | THRESH_BINARY_INV)
        rect_kernel = getStructuringElement(MORPH_RECT, (18, 18))
        dilation = dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = findContours(dilation, RETR_EXTERNAL, CHAIN_APPROX_NONE)
        texts = []

        for cnt in contours:
            x, y, w, h = boundingRect(cnt)
            cropped = img[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped)
            texts.append(text.replace("\n", " "))
        return texts

    while True:
        sleep(1)
        screen = read_screen()
        for entry in screen:
            if check_text(entry):
                print("Problem detected! Reporting...")


def analyze_history():
    from time import sleep

    def get_history():
        from sqlite3 import connect, OperationalError
        from os import getenv
        try:
            db = connect(AppData + "\\Microsoft\\Edge\\User Data\\Default\\History")
        except OperationalError as e:
            print(e)
            return

        entries = db.execute("SELECT term from keyword_search_terms").fetchall()
        db.close()
        for entry in entries:
            entry = entry[0]
            if check_text(entry):
                print("Problem detected! Reporting...")

    while True:
        get_history()
        sleep(60)


# I need to download the policy names from the selected child, and then apply them


from threading import Thread

# Testing Policies
policies = ["HISTORY_WATCH", "KEYS_WATCH", "SCREEN_WATCH"]

# Create the thread definitions
if "KEYS_WATCH" in policies:
    keylogging_thread = Thread(target=keylogging)
    keylogging_thread.start()
if "SCREEN_WATCH" in policies:
    screen_thread = Thread(target=analyze_screen)
    screen_thread.start()
if "HISTORY_WATCH" in policies:
    history_thread = Thread(target=analyze_history())
    history_thread.start()
