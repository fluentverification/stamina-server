from .settings import Settings
from flask import render_template

def create_html_for_response(response, job_status):
	uid = response["id"]
	status = response["status"]
	timeout=5
	return render_template('response.html', uid=uid, status=status, timeout=timeout, Settings=Settings)

def create_html_err(error_msg, redir=True, redir_url="https://staminachecker.org/api/myjobs", after_error_msg = "", timeout=5):
	redir_str = ""
	redir_msg = ""
	return render_template("error.html", redir_url=redir_url, redir=redir, error_msg=error_msg, after_error_msg=after_error_msg, timeout=timeout)

def json_to_table(json):
	html = "<table class=table>\n<tr><th>Key</th><th>Value</th></tr>"
	for k, v in json.items():
		html += f"<tr><td>{k}</td><td>{v}</td></td>"
	return html + "</table>"

def md_list_to_table(lst, first_row_header = True, table_id="table-wrapper"):
	if len(lst) == 0:
		return "<div>Empty Table</div>"
	o = '{'
	c = '}'
	if first_row_header:
		header = "["
		for val in lst[0]:
			header += f"{o}name: gridjs.html(\"{val}\"),id:\"{val}\"{c},"
		header = header[:len(header) - 1] + "]"
		data = "["
		for row in lst[1:]:
			data += "["
			for val in row:
				data += f"gridjs.html(\"{val}\"),"
			data = data[:len(data) - 1] + "],"
		data = data[:len(data) - 1] + "]"
		return f"""<div id={table_id}></div><script>
		new gridjs.Grid({o}
			columns: {header},
			search: true,
			sort: true,
			resizable: true,
			className: {o}
				table: "table"
			{c},
			pagination: {o}
				limit: 20
			{c} ,
			data: {data},
		{c}).render(document.getElementById("{table_id}"));
	</script>"""

def md_list_to_html_table(lst, first_row_header = True):
	if len(lst) == 0:
		return "Empty Table"
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
	
