#!flask/bin/python

from flask import Flask, request, jsonify, Response
import secrets
import sys
from time import time, sleep
from threading import Thread, Lock
import os
from shutil import rmtree
import json
import atexit
import signal

from .settings import Settings, EASTER_EGG
from .Job import Job, stop_all_docker_containers
from .web import *
from .log import *
from .data import *

app = Flask(__name__)

# List of all jobs and their associated
def get_db_connection():
	conn = sqlite3.connect("database.db")
	conn.row_factory = sqlite3.Row
	return conn

def periodically_clean_jobs():
	'''
The target thread which waits every so often and then cleans up old jobs
	'''
	try:
		while True:
			sleep(Settings.CLEANUP_INTERVAL)
			clean_jobs()
	except KeyboardInterrupt:
		# TODO
		pass
		#cur_time = int(time())
		#log(f"Removing temp directory")
		#for uid, job in jobs.items():
			#job.kill()
			#job.clean()

def clean_jobs():
	'''
Clean up old jobs
	'''
	# TODO
	#cur_time = int(time())
	#log("Cleaning old jobs:")
	#uids_to_clean = []
	#for uid, job in jobs.items():
		#age = cur_time - job.creation_time
		#if age >= Settings.MAX_ALLOWED_TIME_PER_JOB:
			#job.kill()
			#log(f"Killing job {uid}")
		#if age >= Settings.MAX_JOB_RETENTION_TIME:
			#ip = job.ip
			#job.clean()
			#uids_to_clean.append(uid)
			# # Clean ip_to_job
			#cur_ip_joblist = ip_to_job[ip]
			#cur_ip_joblist.remove(job)
			#log(f"Removing job {uid}")
			#if len(ip_to_job[ip]) == 0:
				#del ip_to_job[ip]
	#for uid in uids_to_clean:
		#del jobs[uid]
	pass

def get_client_ip():
	# Get the IP if not behind a proxy
	if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
		return request.environ["REMOTE_ADDR"]
	# Get the IP if behind a proxy
	return request.environ["HTTP_X_FORWARDED_FOR"]

def check_request(request, required_fields):
	if not request.is_json:
		return False, "Request should be in JSON format", 415
	request_json = request.get_json()
	for field in required_fields:
		if not field in request_json:
			return False, {"error": f"Field \'{field}\' is required!"}, 400
		
def get_number_jobs(ip = None, conn=None):
	# If IP address is none, we get the total count of jobs on the server
	if conn is None:
		conn = get_db_connection()
	if ip is None:
		count = conn.execute("select count(*) as cnt from jobs;").fetchall()[0]['cnt']
		return count
	else:
		count = conn.execute(
			"select count(*) as cnt from jobs where ip = (?)"
			, (ip)
		).fetchall()[0]['cnt']
		
def create_job(job_id, job_data=None, model_provided=False, prop_provided=False, path="", job_name=None):
	conn = get_db_connection()
	if get_number_jobs(conn=conn) > Settings.MAX_ALLOWED_JOBS:
		return f"Refused: too many total jobs running on server", 503
	ip = get_client_ip()
	job = None
	if get_number_jobs(ip, conn=conn) >= Settings.MAX_REQUESTS_PER_IP:
		log(f"Refusing to create job for IP Address {ip}: They have too many active jobs")
		return f"Refused: Too many jobs for IP address {ip}", 429
	job = Job(job_data, job_id, model_provided, prop_provided, path, ip)
	if job_name is not None:
		job.set_name(job_name)
	# Create entry in the database
	conn.execute("""
insert into jobs (
	job_uid
	, docker_id
	, killed
	, kappa
	, rkappa
	, window
	, name
) values (?, ?, ?, ?, ?, ?, ?)"""
	, (
		job.uid
		, job.container.id
		, job.killed
		, job.kappa
		, job.rkappa
		, job.window
		, job.name
	))
	log(f"Creating job with id {job_id} for IP address {ip}")
	if job.has_inputs:
		return "Created", 201
	else:
		return "No input", 400

def authenticate(uname, passwd):
	'''
This method will eventually allow administrators (such as us) access
	'''
	# This will be a TODO
	return False

def get_random_id():
	secret = secrets.token_urlsafe(16)
	return secret

@app.after_request
def after_request(response):
	header = response.headers
	header['Access-Control-Allow-Origin'] = '*'
	header['Access-Control-Allow-Methods'] = '*'
	return response


# When we upgrade flask version we can just use @app.post
@app.route("/jobs", methods=["POST"])
def post_jobs():
	content_type = request.headers.get("Content-Type")
	# Handle both multipart data (as we would get from a web form,
	# as well as a purely JSON object, in case the API wishes to encode the PRISM
	# and CSL files within the JSON object
	has_json = False
	if content_type == "application/json":
		has_json = True
	elif "multipart/form-data" not in content_type and "application/x-www-form-urlencoded" not in content_type:
		return f"Request not supported! (Requires either 'multipart/form-data', 'application/x-www-form-urlencoded', or 'application/json'; got {content_type})", 415
	conn = get_db_connection()
	# check to see if there is a job ID
	request_data = None
	if has_json:
		request_data = request.json
	else:
		request_data = request.form
	id_key = "id"
	if id_key in request_data:
		query_result = conn.execute("select * from jobs where job_uid = ?", (request_data[id_key])).fetchall()
		if len(query_result) == 1:
			log(f"Providing information about {request_data[id_key]} to ip {get_client_ip()}")
			job_json = {}
			for k, v in query_result[0].items():
				job_json[k] = v
			docker_id = query_result[0]['docker_id']
			killed = query_result[0]['killed'] == 1
			status, logs = get_container_status_logs(docker_id, killed)
			job_json["status"] = status
			job_json["logs"] = logs
			return job_json
		elif len(query_result) == 0:
			return {"error": f"Job with id {request_data['id']} does not exist"}, 404
		else:
			log(f"The query result should have exactly one entry! Instead it has {len(query_result)} entries (uid {request_data[id_key]}")
			return {"error", f"Internal server error. Please report this to Josh."}, 500
	create_key = "create"
	# print(request_data)
	if create_key in request_data: # and request_data[create_key].lower() == "true":
		# Create a job ID
		job_id = get_random_id()
		# Get the model file
		model_provided = ("model_file" in request_data and has_json) or ("model_file" in request.files)
		# Get the properties file
		prop_provided = ("prop_file" in request_data and has_json) or ("prop_file" in request.files)
		# Only create temporary directory if both files provided
		path = ""
		job_name = None
		if model_provided and prop_provided:
			# Create a temporary path
			path = f"{Settings.TMP_DIRECTORY_LOCATION}/{job_id}/"
			if not os.path.isdir(path):
				os.makedirs(path)
			if has_json:
				with open(os.path.join(path, "model.prism"), "w") as m:
					m.write(request_data["model_file"])
				with open(os.path.join(path, "prop.csl"), "w") as p:
					p.write(request_data["prop_file"])
			else:
				# print("Saving files")
				request.files["model_file"].save(os.path.join(path, "model.prism"))
				request.files["prop_file"].save(os.path.join(path, "prop.csl"))
				#job_name = f"{request.files['model_file'].name} / {request.files['prop_file'].name}"
		# Create a job and run it
		response = {}
		response["id"] = job_id
		job_status, job_status_code = create_job(job_id, request_data, model_provided, prop_provided, path, job_name)
		response["status"] = job_status
		#jobs_lock.release()
		if not "from_web" in request_data:
			log(f"IP {get_client_ip()} are not from a web browser, returning as JSON")
			return response, job_status
		elif job_status_code == 429:
			# We don't need to keep garbage files
			rmtree(path)
			return create_html_err(f"Too many jobs for IP Address {get_client_ip()}. (Limit: {Settings.MAX_REQUESTS_PER_IP})")
		elif job_status_code == 503:
			rmtree(path)
			return create_html_err("Server overloaded. Try again later.")
		else:
			log(f"IP {get_client_ip()} are from a web browser. Creating HTML")
			return create_html_for_response(response, job_status)
	# If not, they are trying to get all jobs. Currently, no authentication is supported for this, so it will fail always
	check_request(request, ["username", "password"])
	authenticated = authenticate(request_data["username"], request_data["password"])
	if authenticated:
		#jobs_lock.release()
		return {"error": "Not implemented"}, 500
	else:
		#jobs_lock.release()
		return {"error": "Authentication failure"}, 401

@app.route("/jobs", methods=["GET"])
def get_jobs():
	return {"error": "Unpriviledged access to job list unauthorized"}, 401

@app.route("/myjobs", methods=["GET"])
def get_my_jobs():
	#jobs_lock.acquire()
	ip = get_client_ip()
	log(f"{ip} has asked for their active jobs")
	if not ip in ip_to_job:
		#jobs_lock.release()
		return {"error": f"This IP ({ip}) has no active jobs"}, 400
	my_jobs = []
	for job in ip_to_job[ip]:
		my_jobs.append(job.__json__())
	#jobs_lock.release()
	return jsonify(my_jobs)

@app.route("/myjobs", methods=["DELETE"])
def delete_all_my_jobs():
	#jobs_lock.acquire()
	ip = get_client_ip()
	log(f"{ip} has asked to DELETE all their active jobs")
	if not ip in ip_to_job:
		#jobs_lock.release()
		return {"error": "This IP has no active jobs"}, 400
	jobs_to_delete_count = len(ip_to_job[ip])
	for job in ip_to_job[ip]:
		job.kill()
		pass
	ip_to_job.remove(ip)
	#jobs_lock.release()
	return {"message": f"Success! Deleted {jobs_to_delete_count} jobs!" }

@app.route("/jobs", methods=["DELETE"])
def delete_job():
	jid = request.get_data().decode("utf-8")
	ip = get_client_ip()
	log(f"{ip} has asked to DELETE job with ID '{jid}'")
	if not jid in jobs:
		log("(it does not exist)")
		return "Job does not exist", 400
	j = jobs[jid]
	del jobs[jid]
	if j in ip_to_job[ip]:
		ip_to_job[ip].remove(j)
	if len(ip_to_job[ip]) == 0:
		del ip_to_job[ip]
	return "Success"

@app.route("/rename", methods=["POST"])
def rename_job():
	content_type = request.headers.get("Content-Type")
	request_json = None
	if content_type != "application/json":
		try:
			request_json = json.loads(request.data)
		except Exception:
			return {"error":"Could not rename job with data provided"}, 415
	else:
		request_json = request.get_json()
		# return {"error":f"Requires 'application/json' format, not '{content_type}'"}, 415
	#check_request(request, ["id", "name"])
	jid = request_json["id"]
	name = request_json["name"]
	log(f"{get_client_ip()} wishes to rename job {jid} to name \"{name}\"")
	if not jid in jobs:
		return {"error": f"Job ID {jid} cannot be renamed! It does not exist!"}, 400
	jobs[jid].set_name(name)
	return {"success": f"Successfully renamed job {jid} to {name}"}, 200

@app.route("/about", methods=["GET"])
def about_stamina():
	return """=================================================
STAMINA - the STochiastic Approximate Model-checker for INfinite-state Systems
https://staminachecker.org
=================================================
STAMINA is licensed under the GPLv3 and is developed at Utah State University
=================================================
This version of STAMINA is based on the Storm probabilistic model checking engine, also licensed under the GPLv3 and available at https://stormchecker.org
=================================================
"""

# A little fun
@app.route("/egg", methods=["GET"])
def get_egg():
	return f"There are four lights!\n{EASTER_EGG}"

@app.route("/qapla", methods=["GET"])
def get_qapla():
	return f"<html><body><img src=https://upload.wikimedia.org/wikipedia/en/3/36/TNG-redemption_worf_and_gowron.png></img><br><h1>Qapla!</h1></body></html>"

@app.route("/checkjob", methods=["POST"])
def check_job():
	'''
Assumes the entire body of the request is the uid
	'''
	jid = request.get_data().decode("utf-8")
	log(f"{get_client_ip()} has asked to get information about job {jid}")
	if jid == "":
		return "The /checkjob URI takes a plaintext request format and is intended to be used via terminal!", 415
	if not jid in jobs:
		return f"The ID {jid} does not exist or is not known!", 415
	response = Response(jobs[jid].get_logs())
	# TODO: should probably change this to allow only https://staminachecker.org
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route("/kill", methods=["POST"])
def kill():
	'''
kills a job
	'''
	jid = request.get_data().decode("utf-8")
	log(f"{get_client_ip()} has asked to kill job {jid}")
	if jid == "":
		return "The /kill URI takes a plaintext request format and is intended to be used via terminal!", 415
	if not jid in jobs:
		return f"The ID {jid} does not exist or is not known!", 415
	jobs[jid].kill()
	return "Success", 200
	#del jobs[jid]

#Create cleaning thread
t = Thread(target=periodically_clean_jobs)
t.start()

def exit_handler(signum, frame):
	'''
To be called when the program exits
	'''
	log(f"Exit handler was called with signum {signum}, and frame {frame}")
	stop_all_docker_containers()
	#t.stop()
	rmtree(Settings.TMP_DIRECTORY_LOCATION)
	exit(signum)

atexit.register(exit_handler)
signal.signal(signal.SIGINT, exit_handler)

if __name__=="__main__":
	if "--debug" in sys.argv or "-d" in sys.argv:
		app.run(debug=True,host='0.0.0.0', port=8000)
	else:
		app.run()
