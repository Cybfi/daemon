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
        self.platform = self.kw.platform

    def _get_history_internal(self, browser_path):
        from sqlite3 import connect, OperationalError
        try:
            db = connect(browser_path)

            # noinspection SqlNoDataSourceInspection
            entries = db.execute("SELECT term from keyword_search_terms").fetchall()
            db.close()
            for entry in entries:
                entry = entry[0]
                if _BWLIST.check(entry):
                    gmget("reporter").report(entry)
        except OperationalError:
            return

    def _get_history(self):
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

        posix_supported_browsers = [
            self.kw.appdata + "/microsoft-edge/Default/History",
            self.kw.appdata + "/vivaldi/Default/History",
            self.kw.appdata + "/brave/Default/History",
            self.kw.appdata + "/chromium/Default/History",
            self.kw.appdata + "/google-chrome/Default/History",
            self.kw.appdata + "/opera/History",
        ]
        try:
            if self.platform == "nt":
                for browser_path in windows_supported_browsers:
                    self._get_history_internal(browser_path)
            elif self.platform == "posix":
                for browser_path in posix_supported_browsers:
                    self._get_history_internal(browser_path)

        except OperationalError as e:
            print(e)
            return

    def _THR_FUNC(self):
        while self.active:
            self._get_history()
            sleep(60)
