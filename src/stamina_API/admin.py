import bcrypt

class AdminSettings:
	SALT_SIZE = 12
	MIN_PASSWORD_LENGTH = 12

def hash_passwd(password_plaintext):
	"""
Uses bcrypt to generate a password with the blowfish algorithm
	"""
	return bcrypt.hashpw(password_plaintext, bcrypt.gensalt(AdminSettings.SALT_SIZE))

def check_password(password_plaintext, password_hashed):
	"""
Also use bcrypt to check if a password matches
	"""
	return bcrypt.checkpw(password_plaintext, password_hashed)
	
