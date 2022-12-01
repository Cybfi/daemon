# GLOBALS
import sys

from lib.GlobalManager import gmget, gmset
from lib.KnowWhere import KnowWhere
from lib.Policy import Policy
from lib.RuntimeReporter import RuntimeReporter
from lib.WordList import WordList

_RTMAN: RuntimeReporter = gmset("reporter", RuntimeReporter())
_KNOWWHERE: KnowWhere = gmset("knowwhere", KnowWhere())
_BWLIST: WordList = gmset("bwlist", WordList("https://dl.cybfi.net/badwordlist", _KNOWWHERE.temp + "/badwordlist.txt"))
_BWLIST.download()

def start_policy(pol: Policy):
    pol.start(True)
    return pol


from threading import Thread

# TODO(William): I need to download the policy names from the selected child, and then apply them
# Testing Policies
policies = ["KEYS_WATCH"]

# Create the thread definitions
if "KEYS_WATCH" in policies:
    from lib.Policies.KeylogPolicy import KeylogPolicy

    _KEYLOG: KeylogPolicy = gmset("keylog", KeylogPolicy())
    gmset("keylog_thread", start_policy(_KEYLOG))

if "HISTORY_WATCH" in policies:
    from lib.Policies.HistoryPolicy import HistoryPolicy

    _HISTORY: HistoryPolicy = gmset("history", HistoryPolicy())
    gmset("history_thread", start_policy(_HISTORY))

if "SCREEN_WATCH" in policies:
    from lib.Policies.ScreenPolicy import ScreenPolicy

    _SCREEN: ScreenPolicy = gmset("screen", ScreenPolicy())
    gmset("screen_thread", start_policy(_SCREEN))
