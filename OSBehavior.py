import MemoryObjects

NUM_FRAMES = 8

def mapProcess(line, phys_m):
	process = MemoryObjects.Process(int(line[0]), int(line[1]), int(line[2]))

	remaining = process.text_size
	txt_blks = []

	while remaining > 0:
		if remaining < MemoryObjects.MAX_SIZE:
			txt_blks.append(remaining)
		else:		
			txt_blks.append(MemoryObjects.MAX_SIZE)
		remaining -= MemoryObjects.MAX_SIZE

	open_frames = findOpenFrames(phys_m)
	for blk in txt_blks:
		if not open_frames:
			print('Full physical memory.')
		else:
			process.proc_table.pageToFrame[process.pid] = open_frames[0].fid
			open_frames[0].used = blk
			open_frames.pop(0)

def findOpenFrames(phys_m):
	open_frames = []
	for frame in phys_m.frames:
		if frame.used == 0:
			open_frames.append(frame)
	return open_frames
