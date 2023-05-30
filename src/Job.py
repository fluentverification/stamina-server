#import subprocess
import docker
from settings import Settings
client = docker.from_env()

BASE_IMAGE="ifndefJOSH/sstamina:latest"

METHOD_FLAGS = {
	"iterative": "-I"
	, "reexploring": "-J"
	, "priority": "-P"
}

class Job:
	def __init__(self, data):
		'''
	Data should be in JSON format
		'''
	args = self.__get_args_from_data(data)
		
	def __get_args_from_data(self, data):
		args = []
		method = METHOD_FLAGS[Settings.STAMINA_DEFAULT_METHOD]
		if "method" in data:
			if data["method"].lower() in METHOD_FLAGS:
				method = METHOD_FLAGS[data["method"].lower()]
			else:
				print("Method not supported. Using default")
		args.append(method)
		arg_string = ""
		for arg in args:
			arg_string += f"{arg} "
		return arg_string
