#NOTE TO SELF: tkinter kinda sucks...

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import OSBehavior
import MemorySim

class SpecifyFile(Toplevel):
	def __init__(self, master=None):
		Toplevel.__init__(self, master)
		self.withdraw()
		self.deiconify()
		self.transient(self.master)
		self.grab_set()
		self.filename = StringVar()
		self.createWidgets()
		
	def createWidgets(self):
		filename_label = Label(self, width=60, textvariable=self.filename)
		filename_label.grid(row=0, column=0)
		browse_button = Button(self, width=10, text='Browse', command=(lambda:
			self.filename.set(filedialog.askopenfilename())))
		browse_button.grid(row=0, column=1)
		ok_button = Button(self, text='OK', width=10, command=self.reset)
		ok_button.grid(row=1, column=1, pady=3)
	
	def reset(self):
		self.destroy()
		msim = MemorySim.MemorySim(self.filename.get())
		sim_interface = SimInterface(msim, master = root)
		
class SimInterface(Frame):
	def __init__(self, msim, master = None):
		self.msim = msim
		self.page_names = [] #used for button text
		self.frame_labels = [] #used for coloring
		self.curr_cmd = StringVar()
		self.curr_cmd.set('Step: ' + msim.mem_events[0].strip())
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		frames_frame = Frame(self, relief=RAISED, borderwidth=1)
		frames_frame.grid(row=0, column=0, columnspan=2)
		
		#creates frames visualization
		for frame in self.msim.frames:
			self.page_names.append(StringVar(frame.page.name))
			f_label = Label(frames_frame, text='Frame ' + str(frame.fid))
			f_label.grid(row=frame.fid, column=0, padx=5)
			self.frame_labels.append(f_label)
			f_button = Button(frames_frame, width=30, textvariable=self.page_names[frame.fid])
			f_button.grid(row=frame.fid, column=1, padx=5, pady=3)
		
		#if runs out of commands in queue, warn user
		#otherwise step through the command(first in queue)
		self.STEP = Button(self, width=20, textvariable=self.curr_cmd, command=(lambda: 
			(messagebox.showinfo(title='Finished', message='No more events.  Press reset to run another simulation.')
			if not self.msim.mem_events else self.stepCmd())))
		self.STEP.grid(row=1, column=0, pady=10)
		
		self.RESET = Button(self, width=10, text='Reset', command=self.reset)
		self.RESET.grid(row=1, column=1, padx=2, pady=10)
		
	def stepCmd(self):
		self.resetFrameColors()
		info = self.msim.event_step()
		self.curr_cmd.set(info[0].strip())
		frames = info[1]
		for frame in frames:
			visual_pg_name = self.page_names[frame.fid]
			#detects frees and insertions
			if visual_pg_name.get() == '' and frame.page.name != '':
				self.frame_labels[frame.fid]['fg'] = 'green'
			if visual_pg_name.get() != '' and frame.page.name == '':
				self.frame_labels[frame.fid]['fg'] = 'red'
			visual_pg_name.set(frame.page.name)
			
	def reset(self):
		answer = messagebox.askyesno(
			message='Are you sure you want to reset the sim?  This will erase the current state.',
			icon='question', title='Confirm Reset')
		if answer == False:
			return
		self.destroy()
		top = SpecifyFile(root)
	
	#resets frame label colors to black
	def resetFrameColors(self):
		for label in self.frame_labels:
			label['fg'] = 'black'
			
root = Tk()
root.wm_title("Chau's Memory Simulator")
top = SpecifyFile(root)
root.mainloop()