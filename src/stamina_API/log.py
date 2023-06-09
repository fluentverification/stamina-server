from datetime import datetime
import sys

from .settings import Settings

logfile = None
if Settings.LOG_FILE == "":
	logfile = sys.stdout
else:
	logfile = open(Settings.LOG_FILE, "a")

def log(msg, end="\n"):
	date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
	print(f"[{date_string}]: {msg}", file=logfile, end=end)
