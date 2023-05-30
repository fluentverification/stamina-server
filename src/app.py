#!flask/bin/python

from flask import Flask, request, jsonify
import secrets
import sys

from settings import Settings
from Job import Job

app = Flask(__name__)

# List of all jobs and their associated
jobs = {}

ip_to_job = {}

def get_client_ip():
	# Get the IP if not behind a proxy
	if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
		return request.environ["REMOTE_ADDR"]
	# Get the IP if behind a proxy
	return request.environ["HTTP_X_FORWARDED_FOR"]

def check_request(request, required_fields):
	if not request.is_json:
		return False, {"error": "Request should be in JSON format"}, 415
	request_json = request.get_json()
	for field in required_fields:
		if not field in request_json:
			return False, {"error": f"Field \'{field}\' is required!"}, 400
		
def create_job(job_id, job_data=None):
	if len(jobs) > Settings.MAX_ALLOWED_JOBS:
		return f"Refused: too many total jobs running on server", 503
	ip = get_client_ip()
	if ip in ip_to_job and len(ip_to_job[ip]) > Settings.MAX_REQUESTS_PER_IP:
		return f"Refused: Too many jobs for IP address {ip}", 429
	elif ip in ip_to_job:
		job = Job(job_data, job_id)
		ip_to_job[ip].append(job)
		jobs[job_id] = job
	else:
		job = Job(job_data, job_id)
		ip_to_job[ip] = [job]
		jobs[job_id] = job
	return "Unimplemented", 501

def authenticate(uname, passwd):
	'''
This method will eventually allow administrators (such as us) access
	'''
	# This will be a TODO
	return False

def get_random_id():
	secret = secrets.token_urlsafe(16)
	while secret in jobs:
		secret = secrets.token_urlsafe(16)
	return secret

# When we upgrade flask version we can just use @app.post
@app.route("/jobs", methods=["POST"])
def post_jobs():
	# check to see if there is a job ID
	if not request.is_json:
		return {"error": "Request should be in JSON format"}, 415
	request_json = request.get_json()
	if "id" in request_json:
		return jobs[request_json["id"]].__json__()
	if "create" in request_json and request_json["create"].lower() == "true":
		# Create a job and run it
		response = {}
		job_id = get_random_id()
		response["id"] = job_id
		job_status, job_status_code = create_job(job_id, request_json)
		response["status"] = job_status
		return response, job_status
	# If not, they are trying to get all jobs. Currently, no authentication is supported for this, so it will fail always
	check_request(request, ["username", "password"])
	authenticated = authenticate(request["username"], request["password"])
	if authenticated:
		return jsonify(jobs)
	else:
		return {"error": "Authentication failure"}, 401

@app.route("/jobs", methods=["GET"])
def get_jobs():
	return {"error": "Unpriviledged access to job list unauthorized"}, 401

@app.route("/myjobs", methods=["GET"])
def get_my_jobs():
	ip = get_client_ip()
	if not ip in ip_to_job:
		return {"error": "This IP has no active jobs"}, 400
	my_jobs = []
	for job in ip_to_job[ip]:
		my_jobs.append(job.__json__())
	return jsonify(my_jobs)

@app.route("/myjobs", methods=["DELETE"])
def delete_all_my_jobs():
	ip = get_client_ip()
	if not ip in ip_to_job:
		return {"error": "This IP has no active jobs"}, 400
	jobs_to_delete_count = len(ip_to_job[ip])
	for job in ip_to_job[ip]:
		# TODO: kill job
		pass
	ip_to_job.remove(ip)
	return {"message": f"Success! Deleted {jobs_to_delete_count} jobs!" }

@app.route("/egg", methods=["GET"])
def get_egg():
	return {"egg": f"Easter Egg. Your IP Address is {get_client_ip()}"}

if __name__=="__main__":
	if "--debug" in sys.argv or "-d" in sys.argv:
		app.run(debug=True,host='0.0.0.0', port=8000)
	else:
		app.run()
