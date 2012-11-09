import OSBehavior
import MemoryObjects

frames = []
for i in range(0, OSBehavior.NUM_FRAMES):
	frames.append(MemoryObjects.Frame(i))
phys_m = MemoryObjects.PhysicalM(frames)

filename = input('Enter simulation data file: ')
file = open(filename, 'r')

mem_events = []
for line in file:
	mem_events.append(line)

for raw_cmd in mem_events:
	event = raw_cmd.split(" ")
	print('\nTo process: ' + raw_cmd.strip())
	input('Press enter to step...')
	if len(event) == 3:
		OSBehavior.mapProcess(event, phys_m)
	elif len(event) == 2:
		OSBehavior.freeMemory(event, phys_m)
	for frame in frames:
		print(frame)

file.close()
