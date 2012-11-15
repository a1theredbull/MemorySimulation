#NOTE TO SELF: tkinter kinda sucks...

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import OSBehavior
import MemorySim
import MemoryObjects

def IsInt(input):
	try:
		int(input)
		return True
	except ValueError:
		return False

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
		self.filename_text = Entry(self, width=55, state=DISABLED, textvariable=self.filename)
		self.filename_text.grid(columnspan=4, padx=10)
		browse_button = Button(self, width=10, text='Browse', command=(lambda:
			self.filename.set(filedialog.askopenfilename())))
		browse_button.grid(row=0, column=4)
		ok_button = Button(self, text='OK', width=10, command=self.reset)
		ok_button.grid(row=1, column=4, pady=3)
		
		self.page_size_input = StringVar()
		self.page_size_input.set('512')
		page_size_label = Label(self, text='Frame size')
		page_size_label.grid(row=1, padx=2)
		self.page_size_text = Entry(self, width=10, textvariable=self.page_size_input)
		self.page_size_text.grid(row=1, column=1, padx=2)
		
		self.num_frames_input = StringVar()
		self.num_frames_input.set('8')
		num_frames_label = Label(self, text='# of Frames')
		num_frames_label.grid(row=1, column=2, padx=2)
		self.num_frames_text = Entry(self, width=10, textvariable=self.num_frames_input)
		self.num_frames_text.grid(row=1, column=3, padx=2)
	
	def reset(self):
		if not(IsInt(self.num_frames_input.get()) and IsInt(self.page_size_input.get()) and self.filename.get() != ''):
			messagebox.showinfo(title='Incomplete form', message='Need to specify valid settings before starting simulation!')
			return
		OSBehavior.NUM_FRAMES = int(self.num_frames_input.get())
		MemoryObjects.MAX_SIZE = int(self.page_size_input.get())
		self.destroy()
		msim = MemorySim.MemorySim(self.filename.get())
		sim_interface = SimInterface(msim, master=root)

class PageTable(Toplevel):
	def __init__(self, pid, master=None):
		self.process = [process for process in OSBehavior.processes if process.pid == pid][0]
		Toplevel.__init__(self, master)
		self.withdraw()
		self.deiconify()
		self.transient(self.master)
		self.grab_set()
		self.createWidgets()
		
	def createWidgets(self):
		titleFont = font.Font(family="Arial", size=14)
		pid_label = Label(self, text='Process ' + str(self.process.pid), font=titleFont, justify=CENTER)
		pid_label.grid(row=0, pady=3)
		
		pg_tb_frame = Frame(self, relief=RAISED, borderwidth=1)
		pg_tb_frame.grid(columnspan=3)
		page_label = Label(pg_tb_frame, text='Page')
		page_label.grid(row=0, column=1, padx=5)
		frame_label = Label(pg_tb_frame, text='Frame')
		frame_label.grid(row=0, column=2, padx=5)
		text_label = Label(pg_tb_frame, text='Text')
		text_label.grid(row=1, column=0, padx=5)
		
		#display Text page mapping
		entries = list(self.process.text_pg_table.keys())
		entries.sort()
		offset = 1
		for entry in entries:
			self.key_label = Label(pg_tb_frame, text=entry)
			self.key_label.grid(row=offset, column=1, padx=5)
			self.value_label = Label(pg_tb_frame, text=self.process.text_pg_table[entry])
			self.value_label.grid(row=offset, column=2, padx=5)
			offset += 1
		
		data_label = Label(pg_tb_frame, text='Data')
		data_label.grid(row=offset, column=0, padx=5)
		
		#display Data page mapping
		entries = list(self.process.data_pg_table.keys())
		entries.sort()
		for entry in entries:
			self.key_label = Label(pg_tb_frame, text=entry)
			self.key_label.grid(row=offset, column=1, padx=5)
			self.value_label = Label(pg_tb_frame, text=self.process.data_pg_table[entry])
			self.value_label.grid(row=offset, column=2, padx=5)
			offset += 1
		
class SimInterface(Frame):
	def __init__(self, msim, master=None):
		self.msim = msim
		self.page_names = [] #used for button text
		self.page_sizes = []
		self.frame_labels = [] #used for coloring
		self.curr_cmd = StringVar()
		self.curr_cmd.set('Step: ' + msim.mem_events[0].strip())
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		frames_frame = Frame(self, relief=RAISED, borderwidth=1)
		frames_frame.grid(columnspan=3)
		
		#creates frames visualization
		for frame in self.msim.frames:
			self.page_names.append(StringVar(frame.page.name))
			tempFormat = StringVar() #cannot parse to str and put into StringVar at same time
			tempFormat.set(str(frame.page.used) + '/' + str(frame.page.size)) #read above ^
			self.page_sizes.append(tempFormat)
			
			f_label = Label(frames_frame, text='Frame ' + str(frame.fid))
			f_label.grid(row=frame.fid, padx=5)
			#lambda picks up last loop of frame, have to set frame buffer
			f_button = Button(frames_frame, width=30, textvariable=self.page_names[frame.fid], command=(lambda tempFrame=frame:
				self.showProcessTable(tempFrame.page)))
			f_button.grid(row=frame.fid, column=1, padx=5, pady=3)
			f_size_label = Label(frames_frame, width=7, textvariable=self.page_sizes[frame.fid])
			f_size_label.grid(row=frame.fid, column=2, padx=3)
			
			self.frame_labels.append(f_label)
		
		#if runs out of commands in queue, warn user
		#otherwise step through the command(first in queue)
		self.STEP = Button(self, width=20, textvariable=self.curr_cmd, command=(lambda: 
			(messagebox.showinfo(title='Finished', message='No more events.  Press reset to run another simulation.')
			if not self.msim.mem_events else self.stepCmd())))
		self.STEP.grid(row=1, pady=10)
		
		self.RESET = Button(self, width=10, text='Reset', command=self.reset)
		self.RESET.grid(row=1, column=1, pady=10)
	
	def showProcessTable(self, page):
		if not page.isEmpty:
			top = PageTable(page.pid, master=root)
	
	def stepCmd(self):
		self.resetFrameColors()
		info = self.msim.event_step()
		self.curr_cmd.set(info[0].strip())
		frames = info[1]
		for frame in frames:
			self.page_sizes[frame.fid].set(str(frame.page.used) + '/' + str(frame.page.size))
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