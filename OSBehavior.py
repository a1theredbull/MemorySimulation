import MemoryObjects

NUM_FRAMES = 8
processes = []

def mapProcess(line, phys_m):
	process = MemoryObjects.Process(int(line[0]), int(line[1]), int(line[2]))
	processes.append(process)
	allocateText(process, phys_m)
	allocateData(process, phys_m)
	
#finds open frames for text pages to be allocated to
def allocateText(process, phys_m):
	remaining = process.text_size
	txt_pages = []
	
	count = 0;
	#find number of text pages
	while remaining > 0:
		name = 'P' + str(process.pid) + ' Text Page ' + str(count)
		if remaining < MemoryObjects.MAX_SIZE:
			txt_pages.append(MemoryObjects.Page(process.pid, count, name, remaining, False))
		else:		
			txt_pages.append(MemoryObjects.Page(process.pid, count, name, MemoryObjects.MAX_SIZE, False))
		remaining -= MemoryObjects.MAX_SIZE
		count += 1

	open_frames = findOpenFrames(phys_m)
	
	#map text pages to open frames
	for pg in txt_pages:
		if not open_frames:
			print('Full physical memory.')
		else:
			process.text_pg_table[str(pg.number)] = open_frames[0].fid
			process.text_pages.append(pg)
			open_frames[0].used = pg.used
			open_frames[0].page = pg
			open_frames.pop(0)
	
#finds open frames for data pages to be allocated to
def allocateData(process, phys_m):
	remaining = process.data_size
	dat_pages = []
	
	count = 0;
	#find number of data pages
	while remaining > 0:
		name = 'P' + str(process.pid) + ' Data Page ' + str(count)
		if remaining < MemoryObjects.MAX_SIZE:
			dat_pages.append(MemoryObjects.Page(process.pid, count, name, remaining, False))
		else:		
			dat_pages.append(MemoryObjects.Page(process.pid, count, name, MemoryObjects.MAX_SIZE, False))
		remaining -= MemoryObjects.MAX_SIZE
		count += 1

	open_frames = findOpenFrames(phys_m)
	
	#map data pages to open frames
	for pg in dat_pages:
		if not open_frames:
			print('Full physical memory.')
		else:
			process.data_pg_table[str(pg.number)] = open_frames[0].fid
			process.data_pages.append(pg)
			open_frames[0].used = pg.used
			open_frames[0].page = pg
			open_frames.pop(0)

def findOpenFrames(phys_m):
	open_frames = []
	#detects if page in frame is a placeholder(isEmpty)
	for frame in phys_m.frames:
		if frame.page.isEmpty == True:
			open_frames.append(frame)
	return open_frames
	
def freeMemory(line, phys_m):
	process = findProcess(int(line[0]))[0]
	#frees frame
	for frame in phys_m.frames:
		if frame.page.isEmpty == False and frame.page.pid == process.pid:
			frame.emptyFrame()
	
#finds process in list of processes by id
def findProcess(pid):
	return [process for process in processes if process.pid == pid]
	
