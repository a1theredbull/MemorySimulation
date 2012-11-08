import OSBehavior
import MemoryObjects

frames = []
for i in range(0, OSBehavior.NUM_FRAMES):
	frames.append(MemoryObjects.Frame(i))
phys_m = MemoryObjects.PhysicalM(frames)

filename = input('Enter filename to simulate: ')
file = open(filename, 'r')

mem_events = []
for line in file:
	mem_events.append(line.split(' '))

for event in mem_events:
	if len(event) == 3:
		OSBehavior.mapProcess(event, phys_m)

for frame in frames:
	print(frame)

file.close()
