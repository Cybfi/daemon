from time import sleep

from lib.GlobalManager import gmget
from lib.Policy import Policy
from pyautogui import screenshot
from pytesseract import pytesseract
from numpy import array
from cv2 import COLOR_BGR2GRAY, cvtColor, threshold, THRESH_OTSU, THRESH_BINARY_INV, \
    getStructuringElement, MORPH_RECT, dilate, findContours, RETR_EXTERNAL, \
    CHAIN_APPROX_NONE, boundingRect

from lib.WordList import WordList

_BWLIST: WordList = gmget("bwlist")


class ScreenPolicy(Policy):
    def __init__(self):
        super().__init__()
        self.name = "ScreenPolicy"
        self.active = False

    @staticmethod
    def _read_screen():
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

    def _THR_FUNC(self):
        while True:
            sleep(1)
            screen = self._read_screen()
            for entry in screen:
                if _BWLIST.check(entry):
                    gmget("reporter").report(entry)
