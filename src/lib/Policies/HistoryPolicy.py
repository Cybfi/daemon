from time import sleep

from lib.GlobalManager import gmget
from lib.KnowWhere import KnowWhere
from lib.Policy import Policy
from lib.WordList import WordList

_BWLIST: WordList = gmget("bwlist")

class HistoryPolicy(Policy):

    def __init__(self):
        super().__init__()
        self.name = "HistoryPolicy"
        self.active = False
        self.kw: KnowWhere = gmget("knowwhere")

    def _get_history(self):
        from sqlite3 import connect, OperationalError
        from platform import system
        windows_supported_browsers = [
            self.kw.appdata + "/Microsoft/Edge/User Data/Default/History",
            self.kw.appdata + "/AVG/Browser/User Data/Default/History",
            self.kw.appdata + "/AVAST Software/Browser/User Data/Default/History",
            self.kw.appdata + "/Vivaldi/User Data/Default/History",
            self.kw.appdata + "/BraveSoftware/brave-browser/User Data/Default/History",
            self.kw.appdata + "/Chromium/User Data/Default/History",
            self.kw.appdata + "/Google/Chrome/User Data/Default/History",
            self.kw.appdata + "/../Roaming/Opera Software/Opera Stable/History",
        ]
        try:
            if system() == 'Windows':
                for browser_path in windows_supported_browsers:
                    db = connect(browser_path)

                    # noinspection SqlNoDataSourceInspection
                    entries = db.execute("SELECT term from keyword_search_terms").fetchall()
                    db.close()
                    for entry in entries:
                        entry = entry[0]
                        if _BWLIST.check(entry):
                            gmget("reporter").report(entry)

        except OperationalError as e:
            print(e)
            return

    def _THR_FUNC(self):
        while self.active:
            self._get_history()
            sleep(60)
