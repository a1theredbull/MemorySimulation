MAX_SIZE = 512

class PhysicalM(object):
	frames = []

	def __init__(self, frames):
		self.frames = frames

class Frame(object):
	fid = 0
	used = 0
	size = MAX_SIZE

	def __init__(self, fid):
		self.fid = fid

	def __str__(self):
		return 'Frame ' + str(self.fid) + ': ' + str(self.used) + '/' + str(self.size)

class Process(object):
	pid = 0
	text_size = 0
	data_size = 0

	def __init__(self, pid, text_size, data_size):
		self.pid = pid
		self.text_size = text_size
		self.data_size = data_size
		self.proc_table = ProcessTable()

class ProcessTable(object):
	pageToFrame = {}

class Page(object):
	used = 0
	size = MAX_SIZE
