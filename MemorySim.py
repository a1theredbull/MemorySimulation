import OSBehavior
import MemoryObjects

class MemorySim(object):
	def __init__(self):
		filename = input('Enter simulation data file: ')
		file = open(filename, 'r')
	
		self.mem_events = []
		self.frames = []
		for i in range(0, OSBehavior.NUM_FRAMES):
			self.frames.append(MemoryObjects.Frame(i))
		self.phys_m = MemoryObjects.PhysicalM(self.frames)
	
		for line in file:
			self.mem_events.append(line)
		file.close()
	
	def event_step(self):
		event = self.mem_events[0].split(" ")
		print('\nProcessed: ' + self.mem_events[0].strip())
		if len(event) == 3:
			OSBehavior.mapProcess(event, self.phys_m)
		elif len(event) == 2:
			OSBehavior.freeMemory(event, self.phys_m)
		for frame in self.frames:
			print(frame)
		self.mem_events.pop(0)
