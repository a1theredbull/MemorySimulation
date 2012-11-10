#NOTE TO SELF: tkinter kinda sucks...

from tkinter import *
from tkinter import messagebox
import OSBehavior
import MemorySim

class SimInterface(Frame):
	def createWidgets(self):
		frames_frame = Frame(self, relief=RAISED, borderwidth=1)
		frames_frame.grid(row=0, column=0)
		
		#creates frames visualization
		for frame_num in range(OSBehavior.NUM_FRAMES):
			page_name = StringVar(msim.frames[frame_num].page.name)
			f_label = Label(frames_frame, text='Frame ' + str(frame_num))
			f_label.grid(row=frame_num, column=0, padx=5)
			f_button = Button(frames_frame, width=30, textvariable=page_name)
			f_button.grid(row=frame_num, column=1, padx=5, pady=3)
		
		#if runs out of commands in queue, warn user
		self.STEP = Button(self, text='Step', command=(lambda: 
			(messagebox.showinfo(message='No more events.  Press reset to run another simulation.')
			if not msim.mem_events else msim.event_step())))
		self.STEP.grid(row=1, column=0, pady=10)
		
	
	def __init__(self, msim, master = None):
		self.msim = msim
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		
root = Tk()
root.wm_title("Chau's Memory Simulator")
msim = MemorySim.MemorySim()

sim_interface = SimInterface(msim, master = root)
sim_interface.mainloop()
root.destroy()