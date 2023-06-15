from .settings import Settings

o = '{'
c = '}'

footer = """
<div class=footer>
	<div id="slogo"><b>STAMINA</b></div> is provided as a free service and funded via NSF Grants 1856733, 1856740, and 1900542
</div>
"""

INDEX_CONTENT = f"""
<!DOCTYPE html>
<head>
	<title>STAMINA API</title>
	<link rel="stylesheet" href="https://staminachecker.org/styles.css">
</head>
<body>
	<div class="content">
		<h1>Welcome to the STAMINA API</h1>
		<p>Please visit <a href=https://staminachecker.org/run>https://staminachecker.org/run</a> in order to create and run a Job.</p>
	</div>
	{footer}
</body>
"""

def create_html_for_response(response, job_status):
	uid = response["id"]
	status = response["status"]
	timeout=5
	return f"""
<!DOCTYPE html>
<head>
	<title>Job {uid}</title>
	<link rel="stylesheet" href="https://staminachecker.org/styles.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.kde.org/breeze-icons/icons.css">
	<meta http-equiv="refresh" content="{timeout};url=https://staminachecker.org/api/job?uid={uid}" />
</head>
<body>
	<div class="content">
	<h1>Response from Server</h1>
	(You will be automatically redirected to the page for this current job in <span id=timeout>{timeout}</span> seconds)<br>
	<div class=note>STAMINA has created Job with UID: {uid}<br>(Job status {status})</div>
	<p>Do not lose this number. This is how you access details for this job later. Jobs will be killed after {Settings.MAX_JOB_RETENTION_TIME} seconds ({Settings.MAX_JOB_RETENTION_TIME / 60} minutes). Results for this job will be purged from our systems after {Settings.CLEANUP_INTERVAL / 60 / 60} hours. Only {Settings.MAX_REQUESTS_PER_IP} jobs are allowed per user.</p>
	<h2>How to access your job</h2>
	<ul>
		<li>Access a list of all of your active jobs at <a href="https://staminachecker.org/api/myjobs">https://staminachecker.org/api/myjobs</a></li>
		<li>Access information for this job specifically at <a href="https://staminachecker.org/api/job?uid={uid}">https://staminachecker.org/api/job?uid={uid}</a></ul>
	</ul>
	<h2>Some things to be aware of</h2>
	<ul>
		<li>This page <b>does not report</b> errors recieved by STAMINA or Storm. You will have to view the logs page for the current job.</li>
		<li>The results provided here are under no warranty, and are provided as a service by Fluent Verification and Utah State University, who are not liable for any innacuracies.</li>
	</ul>
	<a class="button" href="https://staminachecker.org/api/myjobs"><i class="icon icon_go-next"></i>See My Jobs</a>
	<a class="button" href="https://staminachecker.org/api/job?uid={uid}"><i class="icon icon_go-next"></i>See Current Jobs</a>
	<div>
<script>
let timeout = document.getElementById('timeout');
var time = {timeout};

function reduceTime() {o}
	if (time == 0) return;
	time--;
	timeout.innerHTML = time;
	setTimeout(reduceTime, 1000);
{c}

reduceTime();
</script>
{footer}
</body>
"""

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
