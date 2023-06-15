from multiprocessing import Lock
from multiprocessing.managers import AcquirerProxy, BaseManager, DictProxy
import dill

def get_shared_state(host, port, key):
	shared_jobs_dict = {}
	shared_i2j_dict = {}
	shared_lock = Lock()
	manager = BaseManager((host, port), key)
	manager.register("get_jobs_dict", lambda: shared_jobs_dict, DictProxy)
	manager.register("i2j_dict", lambda: shared_i2j_dict, DictProxy)
	manager.register("get_lock", lambda: shared_lock, AcquirerProxy)
	try:
		manager.get_server()
		manager.start()
	except OSError:
		manager.connect()
	return manager.get_jobs_dict(), manager.i2j_dict(), manager.get_lock()
