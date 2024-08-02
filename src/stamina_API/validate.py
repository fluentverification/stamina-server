import werkzeug

def validate_model_file(mod_file : werkzeug.datastructures.FileStorage) -> bool:
	if not mod_file.filename.endswith((".pm", ".sm", ".prism", ".model")):
		return False
	try:
		file_text : str = mod_file.read().encode("utf-8")
		strped_text = file_text.strip()
		if not strped_text.isprintable():
			return False
		if not strped_text.startswith("ctmc"):
			return False
		if (not "module" in strped_text) or (not "endmodule" in strped_text):
			return False
		return True
	except Exception:
		return False

def validate_prop_file(prop_file : werkzeug.datastructures.FileStorage) -> bool:
	if not prop_file.filename.endswith((".csl", ".prop", ".pctl")):
		return False
	try:
		file_text : str = prop_file.read().encode("utf-8")
		strped_text = file_text.strip()
		if not strped_text.isprintable():
			return False
		return True
	except Exception:
		return False
