#!/usr/bin/env python3
import requests
import sys

ADDRESS="http://127.0.0.1"
PORT="5000"
SUB_ADDR="jobs"

def create_job_from_local(m_file, p_file, pure_json=False):
	obj = {}
	model_file_contents = None
	prop_file_contents = None
	files = {
		"model_file": open(m_file, 'r')
		, "prop_file": open(p_file, 'r')
	}
	if pure_json:
		with open(m_file, 'r') as m:
			model_file_contents = m.read()
		with open(p_file, 'r') as p:
			prop_file_contents = p.read()
		obj["model_file"] = model_file_contents
		obj["prop_file"] = prop_file_contents
	obj["create"] = "true"
	obj["method"] = "reexploring"
	if pure_json:
		return requests.post(f"{ADDRESS}:{PORT}/{SUB_ADDR}", json=obj)
	else:
		return requests.post(f"{ADDRESS}:{PORT}/{SUB_ADDR}", data=obj, files=files)

if __name__=="__main__":
	if len(sys.argv) < 3:
		print("Needs at least two arguments")
		exit(1)
	m_file = sys.argv[1]
	p_file = sys.argv[2]
	json = "--json" in sys.argv
	print(create_job_from_local(m_file, p_file, json).content)
	
