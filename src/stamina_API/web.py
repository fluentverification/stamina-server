from .settings import Settings
from flask import render_template

o = '{'
c = '}'

footer = """
<div class=footer>
	<div id="slogo"><b>STAMINA</b></div> is provided as a free service and funded via NSF Grants 1856733, 1856740, and 1900542
</div>
"""

def create_html_for_response(response, job_status):
	uid = response["id"]
	status = response["status"]
	timeout=5
	return render_template('response.html', uid=uid, status=status, timeout=timeout, Settings=Settings)

def create_html_err(error_msg, redir=True, redir_url="https://staminachecker.org/api/myjobs", after_error_msg = ""):
	redir_str = ""
	redir_msg = ""
	if redir:
		redir_str = f"""<meta http-equiv="refresh" content="5;url={redir_url}" />"""
		redir_msg = f"""<div>Redirecting to {redir_url}</div>"""
	return f"""
<!DOCTYPE html>
<head>
	<title>ERROR: {error_msg}</title>
	<link rel="stylesheet" href="https://staminachecker.org/styles.css">
	{redir_str}
</head>
<body>
	<div class="content">
	<h1>Response from Server</h1>
	<div class="error">Got error from server:<br>{error_msg}</div>
	{redir_msg}
	<div>
	{after_error_msg}
	</div>
	{footer}
</body>
"""

def json_to_table(json):
	html = "<table class=table>\n<tr><th>Key</th><th>Value</th></tr>"
	for k, v in json.items():
		html += f"<tr><td>{k}</td><td>{v}</td></td>"
	return html + "</table>"

def md_list_to_table(lst, first_row_header = True):
	if len(lst) == 0:
		return "<div>Empty Table</div>"
	html = "<table class=table>"
	rng = None
	if first_row_header:
		rng = range(1, len(lst))
		html += "<tr>"
		for item in lst[0]:
			html += f"<th>{item}</th>"
		html += "</tr>"
	else:
		rng = range(len(lst))
	for i in rng:
		row = lst[i]
		html += "<tr>"
		for item in row:
			html += f"<td>{item}</td>"
		html += "</tr>"
	return html + "</table>"
	
