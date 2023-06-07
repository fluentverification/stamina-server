import os

class Settings:
	# API Settings
	MAX_REQUESTS_PER_IP = 3
	MAX_ALLOWED_JOBS = 100
	MAX_ALLOWED_TIME_PER_JOB = 5 * 60 # 5 minutes
	MAX_ALLOWED_MEMORY="500m" # 500 megabytes
	#MAX_JOB_RETENTION_TIME = 10 * 60 # 10 minutes 
	MAX_JOB_RETENTION_TIME = 10 * 60 * 60 # 10 hours
	#CLEANUP_INTERVAL = 5 * 60 # Five minutes
	LOG_FILE = ""
	CLEANUP_INTERVAL = 24 * 60 * 60 # 24 hours
	TMP_DIRECTORY_LOCATION = os.path.join(os.getcwd(), "api_data")
	# STAMINA Settings
	STAMINA_DEFAULT_METHOD = "reexploring"

EASTER_EGG = """
                                _____
                       __...---'-----`---...__
                  _===============================
 ______________,/'      `---..._______...---'
(____________LL). .    ,--'
 /    /.---'       `. /
'--------_  - - - - _/
          `~~~~~~~~'
"""
