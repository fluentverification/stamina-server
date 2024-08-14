import werkzeug
import os

def validate_model_file(mod_file : werkzeug.datastructures.FileStorage) -> bool:
	print("called me")
	mod_file.seek(0, os.SEEK_SET)
	if not mod_file.filename.endswith((".pm", ".sm", ".prism", ".model")):
		return False
	try:
		file_text : str = mod_file.read().decode("utf-8")
		strped_text = file_text.strip()
		if not strped_text.replace("\n", "").replace("\r", "").replace("\t", "").isprintable():
			return False
		# if not strped_text.startswith("ctmc"):
		if not "ctmc" in strped_text:
			return False
		if (not "module" in strped_text) or (not "endmodule" in strped_text):
			return False
		return True
	except Exception as e:
		return False

def validate_prop_file(prop_file : werkzeug.datastructures.FileStorage) -> bool:
	print("called me")
	prop_file.seek(0, os.SEEK_SET)
	if not prop_file.filename.endswith((".csl", ".prop", ".pctl", ".props")):
		return False
	try:
		file_text : str = prop_file.read().decode("utf-8")
		strped_text = file_text.strip()
		if not strped_text.replace("\n", "").replace("\r", "").replace("\t", "").isprintable():
			return False
		return True
	except Exception as e:
		return False
