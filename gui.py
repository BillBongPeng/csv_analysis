from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import sys
import numpy as np
import datatable as dt


global checkOpen, checkPercent, checkCluster, checkCh1, checkCh2
checkOpen= False
checkPercent = False
checkCluster = False
checkCh1 = False
checkCh2 = False

#HomePage
class HomePage(Frame):

	
	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.master = master
		self.init_window()
		
		
	
	def init_window(self):
	
		self.master.title("Analysis")
		#self.pack(fill=BOTH, expand=1)
		
		#Menu Initialization
		menu = Menu(self.master)
		self.master.config(menu=menu)
		
		#Menu Option File
		files = Menu(menu)
		menu.add_cascade(label="File", menu=files)
		#Opening Files
		files.add_command(label="Open", command = self.open_file)
		#Saving the Report
		files.add_command(label="Save", command = self.save_file)
		
		#Menu Option Analyze	
		analyze = Menu(menu)
		menu.add_cascade(label="Calculate", menu=analyze)
		analyze.add_command(label="Run", command = self.run_calculation)
		analyze.add_command(label="Percentage", command = self.run_percentage)
		#TODO append command for calculating based on client need
		analyze.add_command(label="Add")
		#TODO append command for adding new calculation method
		analyze.add_command(label="Edit", command = self.popup_window)
		#TODO append command for editing calculations
		analyze.add_command(label="Delete")
		#TODO append command for deleting if needed

		#Menu Option Settings
		settings = Menu(menu)
		menu.add_cascade(label="Settings", menu=settings)
		#TODO append command for Update Calcuations (If necessary)
		settings.add_command(label = "Update")
		#TODO append command for About Developer
		settings.add_command(label = "About", command = self.about_dev)

		#Using Labels with Grid For Displaying Results
		#TitleLabel
	def run_calculation(self):
		#tree = Treeview(self.master, columns=(Calc_title, Result_title))
		#tree.heading('#0', text=Calc_title)
		#tree.heading('#1', text=Result_title)
		#col0 = tree.column('#0', stretch=True)
		#col1 = tree.column('#1', stretch=True)
		#tree.grid(row = 5, columnspan =2, sticky="nsew")
		#treeview = tree
		#tree.insert('','end','gp_nm1',text = Calc_one_name,values = Calc_one_value)
		#tree.insert('','end','gp_nm2',text = Calc_two_name, values = Calc_two_value)
		#tree.insert('','end','gp_nm3',text = Calc_three_name, values = Calc_three_value)
		#tree.insert('','end','gp_nm4',text = Calc_four_name, values = Calc_four_value)
		
		#Max and Min values are only the Max and Min of the Respective columns, and in no association with the actual datapoint
		meanVal = self.ds_frame.groupby(['Cluster']).mean()
		self.mean_list = [meanVal.columns.values.tolist()]+meanVal.values.tolist()

		maxVal = self.ds_frame.groupby(['Cluster']).max()
		self.max_list = [maxVal.columns.values.tolist()]+maxVal.values.tolist()

		minVal = self.ds_frame.groupby(['Cluster']).min()
		self.min_list = [minVal.columns.values.tolist()]+ minVal.values.tolist()
		
		medianVal = self.ds_frame.groupby(['Cluster']).median()
		self.median_list = [medianVal.columns.values.tolist()]+medianVal.values.tolist()
		
		
		

	#A Simple Calculation based on the percentage of the cluster and the total number of datapoints
	def run_percentage(self):
		global checkOpen, checkPercent
		#Error Check for datapoint_count
		if checkOpen == True:
			checkPercent = True
			#When datapoint_count exists	
			Calc_title = "Name"
			Result_title = "Percentage(%)"
			calc_name = ["Cluster 1 Percentage","Cluster 2 Percentage","Cluster 3 Percentage","Cluster 4 Percentage"]
			tree = Treeview(self.master, columns=(Calc_title, Result_title))
			tree.heading('#0', text=Calc_title)
			tree.heading('#1', text=Result_title)
			col0 = tree.column('#0', stretch=True)
			col1 = tree.column('#1', stretch=True)
			tree.grid(row = 5, columnspan =2, sticky="nsew")
			treeview = tree
			
			for x in range(len(calc_name)):
				tree.insert('','end', calc_name[x], text=calc_name[x], values = self.ratios[x] )
			
		else:
			try:
				getattr(HomePage, 'datapoint_count')
			except AttributeError:
				messagebox.showinfo("Error", "No File Opened")

			


	def exit_program(self):
		exit()
	
	#Method of opening file, if needed to open multiple files, use a splitlist since askopenfilename returns a string 
	def open_file(self):
		global checkOpen 
		checkOpen = True
		file_name = filedialog.askopenfilename(initialdir = "/home/yipeng/analysis", title = "Select File", filetypes = (("csv files","*.csv"),("all files","*.*")), multiple = True)
		#file_directory = filedialog.askdirectory()
		#print(file_name)	
		file_label = Label(self, text=file_name)
		file_label.pack()
		Cluster_title = "Cluster Number"
		Datapoint_title = "Datapoint Count"
		tree = Treeview(self.master, columns=(Cluster_title,Datapoint_title))
		tree.heading('#0', text=Cluster_title)
		tree.heading('#1', text=Datapoint_title)
		#tree.heading('#2', text=Calc_title)
		col0 = tree.column('#0', stretch=True)
		col1 = tree.column('#1', stretch=True)
		tree.grid(row = 5, columnspan =2, sticky="nsew")
		treeview = tree

		placeholder = []
		for files in file_name:
			ds = pd.read_csv(files,index_col = None, header = 0)
			placeholder.append(ds)
		self.ds_frame = pd.concat(placeholder, axis = 0, ignore_index = True)
		#ds_frame = pd.DataFrame(ds)
		ds_cluster = self.ds_frame[self.ds_frame.columns[2]]
		ds_cluster = ds_cluster.values
		cluster_num, self.datapoint_count = np.unique(ds_cluster, return_counts = True)
		self.cluster_frequency = np.asarray((cluster_num, self.datapoint_count))
		self.total_datapoint = sum(self.datapoint_count)
		self.cnt_gone = self.datapoint_count[0]
		self.cnt_gtwo = self.datapoint_count[1]
		self.cnt_gthree = self.datapoint_count[2]
		self.cnt_gfour = self.datapoint_count[3]
		self.ratios = []
		for x in range(len(self.datapoint_count)):
			self.ratios.append(self.datapoint_count[x]/self.total_datapoint*100)

		for x in range(len(cluster_num)):
			tree.insert('','end',cluster_num[x], text = cluster_num[x], values = self.datapoint_count[x])

		tree.insert('','end','total', text= 'Total', values = self.total_datapoint)
		#Seaborn Plot
		self.scatterplot = sb.lmplot(x='Ch1 Amplitude', y='Ch2 Amplitude', data = self.ds_frame, fit_reg= False)
		plt.show()
		
		
	def save_file(self):
		form = '{:<10}|{:<10}\n'
		
		
		global checkOpen, checkPercent
		if checkOpen == True:
			if checkPercent == True:
				self.scatterplot.savefig('ExperimentScatterPlot', format= 'png')
				with open('Report.txt', 'w') as output:
					output.write("Experiment Report\n")

					output.write("\nTotal Datapoints\n")
					output.write(str(self.total_datapoint)+"\n")

					output.write("\nCluster Frequency\n"+"Cluster Name          Count \n")
					for x in range(3):
						output.write(str(self.cluster_frequency[0][x])+"                ")
						output.write(str(self.cluster_frequency[1][x])+"\n")

					output.write("\nCluster Ratio\n")
					output.writelines(str(self.ratios)+"\n")

					output.write("\nMin Value\n")
					for i in self.min_list:
						output.write(form.format(*i))

					output.write("\nMax Value\n")
					for i in self.max_list:
						output.write(form.format(*i))

					output.write("\nMedian Value\n")
					for i in self.median_list:
						output.write(form.format(*i))

					output.write("\nMean Value\n")
					for i in self.mean_list:
						output.write(form.format(*i))
					
					output.close()
				messagebox.showinfo("Report", "Report has been saved!")
			else:
				try:
					getattr(HomePage,'ratios')
				except AttributeError:
					messagebox.showinfo("Error", "Please Run Ratios First")
		else:
			try:
				getattr(HomePage, 'scatterplot')
			except AttributeError:
				messagebox.showinfo("Error", "No File Opened")
	

	#Method of About Developer
	def about_dev(self):
		messagebox.showinfo("About Developer", "Developed By Neusoft America")

	def popup_window(self):
		popup = Toplevel()
		v = IntVar()
		popup.wm_title("Select")
		Label(popup,text="Select Configuration Count Method", justify = LEFT).pack()
		self.cluster_button = Radiobutton(popup, text="Cluster", variable=v, value=1, command = self.change_selection)
		self.cluster_button.pack(anchor=W)
		self.ch1_button = Radiobutton(popup, text="Ch1", variable=v, value=2,  command = self.change_selection)
		self.ch1_button.pack(anchor=W)
		self.ch2_button = Radiobutton(popup, text="Ch2", variable=v, value=3,  command = self.change_selection)
		self.ch2_button.pack(anchor=W)
		self.run_button = Button(popup, text="Run", command = self.on_run)

	def change_selection(self):
		global checkCluster, checkCh1, checkCh2
		if self.cluster_button:
			checkCluster = True
		elif self.ch1_button:
			checkCh1 = True
		elif self.ch2_button:
			checkCh2 = True

	#
	#def on_run(self):
		#global checkCluster, checkCh1, checkCh2
		#if checkCluster = True:

		#elif checkCh1 = True:

		#elif checkCh2 = True:

#class SelectionWindow(Window):

	
	#def __init__(self, master):
		#Window.__init__(self,master)
		#self.create_tree() 

	#def create_window(self):
		






root = Tk()
root.geometry("600x200")
app = HomePage(root)
root.mainloop()
