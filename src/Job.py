'''
TODO: 
- Use Flask's file uploads (https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/) methods rather than trying to take file content as a string.
- Save file into a folder <cwd>/<job-id>/model.prism, etc for prop file
- Mount that folder into the docker container
'''
import docker
from flask import jsonify
from time import time
from shutil import rmtree
import os

from settings import Settings
from log import log

client = docker.from_env()

BASE_IMAGE="ifndefjosh/sstamina:qest23"
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

def safe_terminal_string(contents):
	contents = contents.replace("\\", "\\\\")
	contents = contents.replace('"', '\\"')
	contents = contents.replace("'", "\\'")
	contents = contents.replace("\n", "\\n")
	return contents

def create_command_write_file(contents, filename):
	contents = safe_terminal_string(contents)
	return f"tee {filename} < \"{contents}\""

def stop_all_docker_containers():
	for container in client.containers.list():
		log(f"Stopping container {container.name}...", end="")
		container.stop()
		log(done)
	client.containers.prune()

class Job:
	def __init__(self, data, uid, model_provided=True, prop_provided=True, path="", ip=None, in_container_path="/tmp/", create_tra_file=False):
		'''
	Data should be in JSON format
		'''
		self.method = None
		self.kappa = None
		self.rkappa = None
		self.window = None
		self.creation_time = int(time())
		self.path = path
		self.ip = ip
		self.name = "Untitled Job"
		self.additional_logs = ""
		self.killed = False
		self.create_tra_file = create_tra_file
		args = self.__get_args_from_data(data)
		# create model.prism and properties.csl in docker container
		if model_provided and prop_provided:
			if path == "":
				print("Path should not be \"\"!")
				return
			#mod = create_command_write_file(data["model_file"], "model.prism")
			#prop = create_command_write_file(data["prop_file"], "properties.csl")
			#mount = docker.types.Mount(target=in_container_path, source=self.path, read_only=True)
			self.command = f"{SSTAMINA} {args} {in_container_path}/model.prism {in_container_path}/prop.csl" # f"sstamina {args} model.prism properties.csl"
			if self.create_tra_file:
				self.command += " -a transitions.tra"
			#full_command = f"{mod} && {prop} \\\n && cat model.prism"
			#print(f"Full command for docker container:\n{full_command}")
			self.has_inputs = True
			self.container = client.containers.run(BASE_IMAGE
				, self.command
				, detach=True
				, volumes={path:{'bind':in_container_path, 'mode':'rw'}}
			)
			self.name = self.container.name
		# If model and properties files not specified, just get STAMINA version
		else:
			print("Either model or property file not provided!")
			self.command = f"{SSTAMINA} -v"
			self.has_inputs = False
			self.container = None
		self.uid = uid

	def clean(self):
		if os.path.isdir(self.path):
			rmtree(self.path)
	
	def has_tra_file(self):
		return self.create_tra_file and self.get_status() == "exited"

	def set_name(self, name):
		self.name = name

	def get_status(self):
		self.container.reload()
		if self.killed:
			return "killed"
		else:
			return self.container.status

	def __str__(self):
		data = self.__json__()
		return jsonify(data)
	
	def __json__(self, **options):
		data = {}
		data["uid"] = self.uid
		if self.container is not None:
			data["status"] = self.get_status() # self.container.status if not self.killed else "killed"
			data["logs"] = self.get_logs()
			data["command"] = self.command
			data["method"] = self.method
			data["kappa"] = self.kappa
			data["rkappa"] = self.rkappa
			data["window"] = self.window
			data["name"] = self.name
		else:
			data["status"] = "nonexistent"
			data["message"] = "A model or properties file (which is required) was not provided"
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
		return self.container.logs().decode("utf-8") + f"\n{self.additional_logs}"

	def kill(self):
		if not self.get_status in ["killed", "exited"]:
			return
		self.container.stop()
		self.clean()
		self.additional_logs = "Killed."
		self.killed = True
