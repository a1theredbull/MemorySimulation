MAX_SIZE = 512

class PhysicalM(object):
	frames = []

	def __init__(self, frames):
		self.frames = frames

class Frame(object):
	def __init__(self, fid):
		self.fid = fid
		self.page = Page(0, 0, '', 0, True)
		self.used = 0
		self.size = MAX_SIZE

	def __str__(self):
		return 'Frame ' + str(self.fid) + ': ' + str(self.used) + '/' + str(self.size) + \
				' ' + (self.page.name if self.page != None else ' ')
		
	def emptyFrame(self):
		self.used = 0
		self.page.resetPage()

class Process(object):
	def __init__(self, pid, text_size, data_size):
		self.pid = pid
		self.text_size = text_size
		self.data_size = data_size
		self.text_pages = [] #holds Page objects
		self.data_pages = [] #holds Page objects
		self.text_pg_table = {} #maps text page numbers to frame numbers
		self.data_pg_table = {} #maps data page numbers to frame numbers

class Page(object):
	def __init__(self, pid, number, name, used, isEmpty):
		self.pid = pid
		self.number = number
		self.name = name
		self.used = used
		self.size = MAX_SIZE
		self.isEmpty = isEmpty #flag to use as placeholder for empty pages
		
	def resetPage(self):
		self.used = 0
		self.isEmpty = True
		self.name = ''
