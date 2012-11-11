import OSBehavior
import MemoryObjects

class MemorySim(object):
	def __init__(self, filename):
		file = open(filename, 'r')
	
		#stores memory event strings and initialized frames
		self.mem_events = []
		self.frames = []
		for i in range(0, OSBehavior.NUM_FRAMES):
			self.frames.append(MemoryObjects.Frame(i))
		self.phys_m = MemoryObjects.PhysicalM(self.frames)
		for line in file:
			self.mem_events.append(line)

		file.close()
	
	#returns state of memory after each step
	def event_step(self):
		event = self.mem_events[0].split(" ")
		print('\nProcessed: ' + self.mem_events[0].strip())
		#detects type of command(new process or halting process)
		if len(event) == 3:
			OSBehavior.mapProcess(event, self.phys_m)
		elif len(event) == 2:
			OSBehavior.freeMemory(event, self.phys_m)
		#prints state of frames
		for frame in self.frames:
			print(frame)
			
		#returns state of memory(used for GUI)
		info = []
		self.mem_events.pop(0)
		if not self.mem_events:
			info.append('Finished')
		else:
			info.append('Step: ' + self.mem_events[0])
		info.append(self.frames)
		return info
