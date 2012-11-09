import MemoryObjects

NUM_FRAMES = 8
processes = []

def mapProcess(line, phys_m):
	process = MemoryObjects.Process(int(line[0]), int(line[1]), int(line[2]))
	processes.append(process)
	
	remaining = process.text_size
	txt_pages = []

	count = 0;
	#find number of text pages
	while remaining > 0:
		name = 'P' + str(process.pid) + ' Text Page ' + str(count)
		if remaining < MemoryObjects.MAX_SIZE:
			txt_pages.append(MemoryObjects.Page(process.pid, name, remaining))
		else:		
			txt_pages.append(MemoryObjects.Page(process.pid, name, MemoryObjects.MAX_SIZE))
		remaining -= MemoryObjects.MAX_SIZE
		count += 1

	open_frames = findOpenFrames(phys_m)
	
	#map text pages to open frames
	for pg in txt_pages:
		if not open_frames:
			print('Full physical memory.')
		else:
			process.proc_table.pageToFrame[process.pid] = open_frames[0].fid
			process.text_pages.append(pg)
			open_frames[0].used = pg.used
			open_frames[0].page = pg
			open_frames.pop(0)

def findOpenFrames(phys_m):
	open_frames = []
	for frame in phys_m.frames:
		if frame.page is None:
			open_frames.append(frame)
	return open_frames
	
def freeMemory(line, phys_m):
	process = findProcess(int(line[0]))[0]
	for frame in phys_m.frames:
		if frame.page != None and frame.page.pid == process.pid:
			frame.emptyFrame()
	
def findProcess(pid):
	return [process for process in processes if process.pid == pid]
	
