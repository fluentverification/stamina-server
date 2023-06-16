import bcrypt

class AdminSettings:
	SALT_SIZE = 12
	MIN_PASSWORD_LENGTH = 12

def hash_passwd(password_plaintext):
	"""
Uses bcrypt to generate a password with the blowfish algorithm
	"""
	return bcrypt.hashpw(password_plaintext, bcrypt.gensalt(AdminSettings.SALT_SIZE)).decode("utf-8")

def check_password(password_plaintext, password_hashed):
	"""
Also use bcrypt to check if a password matches
	"""
	print(f"{password_plaintext}, {password_hashed}")
	password_plaintext = password_plaintext.encode("utf-8")
	password_hashed = password_hashed.encode("utf-8")
	return bcrypt.checkpw(password_plaintext, password_hashed)
	
