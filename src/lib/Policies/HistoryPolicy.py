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
        try:
            # this needs to be multi-browser compatible
            # check default browser
            db = connect(self.kw.appdata + "/Microsoft/Edge/User Data/Default/History")
        except OperationalError as e:
            print(e)
            return

        # noinspection SqlNoDataSourceInspection
        entries = db.execute("SELECT term from keyword_search_terms").fetchall()
        db.close()
        for entry in entries:
            entry = entry[0]
            if _BWLIST.check(entry):
                gmget("reporter").report(entry)

    def _THR_FUNC(self):
        while self.active:
            self._get_history()
            sleep(60)
