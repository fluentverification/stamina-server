import docker
from flask import jsonify

from settings import Settings

client = docker.from_env()

BASE_IMAGE="ifndefjosh/sstamina:v3.0_06330ce720011b1a4a1e8e1c740a601fa8d137ed"
client.images.pull(BASE_IMAGE)

SSTAMINA="/opt/stamina-storm/build/sstamina"

METHOD_FLAGS = {
	"iterative": "-I"
	, "reexploring": "-J"
	, "priority": "-P"
}

def check_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

class Job:
	def __init__(self, data, uid):
		'''
	Data should be in JSON format
		'''
		self.method = None
		self.kappa = None
		self.rkappa = None
		self.window = None
		args = self.__get_args_from_data(data)
		# TODO: create model.prism and properties.csl in docker container
		self.command = f"{SSTAMINA} {args} --help" # f"sstamina {args} model.prism properties.csl"
		self.container = client.containers.run(BASE_IMAGE, self.command, detach=True)
		self.uid = uid
		
	
	def __str__(self):
		data = self.__json__()
		return jsonify(data)
	
	def __json__(self, **options):
		data = {}
		data["uid"] = self.uid
		data["status"] = self.container.status
		data["command"] = self.command
		data["method"] = self.method
		data["kappa"] = self.kappa
		data["rkappa"] = self.rkappa
		data["window"] = self.window
		data["logs"] = self.container.logs()
		return data

	def __get_args_from_data(self, data):
		'''
	Currently only supports:
	   - kappa
	   - kappa reduction factor
	   - window
	   - method
		'''
		if data is None:
			return ""
		args = []
		method = METHOD_FLAGS[Settings.STAMINA_DEFAULT_METHOD]
		self.method = Settings.STAMINA_DEFAULT_METHOD
		if "method" in data:
			if data["method"].lower() in METHOD_FLAGS:
				method = METHOD_FLAGS[data["method"].lower()]
				self.method = data["method"]
			else:
				print("Method not supported. Using default")
		args.append(method)
		self.kappa = "STAMINA_DEFAULT"
		if "kappa" in data:
			if check_float(data["kappa"]):
				args.append(f"-k {data['kappa']}")
				self.kappa = data['kappa']
		self.rkappa = "STAMINA_DEFAULT"
		if "rkappa" in data:
			if check_float(data["rkappa"]):
				args.append(f"-r {data['rkappa']}")
				self.rkappa = data["rkappa"]
		self.window = "STAMINA_DEFAULT"
		if "window" in data:
			if check_float(data["window"]):
				args.append(f"-w {data['window']}")
				self.window = data["window"]
		arg_string = ""
		for arg in args:
			arg_string += f"{arg} "
		return arg_string

	def get_logs(self):
		return self.container.logs()

	def kill(self):
		self.container.stop()
