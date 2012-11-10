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
		self.page = Page(0, '', 0, True)

	def __str__(self):
		return 'Frame ' + str(self.fid) + ': ' + str(self.used) + '/' + str(self.size) + \
				' ' + (self.page.name if self.page != None else ' ')
		
	def emptyFrame(self):
		self.used = 0
		self.page.resetPage()

class Process(object):
	pid = 0

	def __init__(self, pid, text_size, data_size):
		self.pid = pid
		self.text_size = text_size
		self.data_size = data_size
		self.text_pages = []
		self.data_pages = []
		self.proc_table = ProcessTable()

class ProcessTable(object):
	pageToFrame = {}

class Page(object):
	used = 0
	size = MAX_SIZE
	
	def __init__(self, pid, name, used, empty):
		self.pid = pid
		self.name = name
		self.used = used
		self.empty = empty
		
	def resetPage(self):
		self.used = 0
		self.empty = True
		self.name = ''
