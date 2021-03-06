import sys
import os
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import math as mt
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time as time
import string as st
import statistics as stat
from matplotlib import rcParams
import random as random
import shutil
from pathlib import Path
import re as re


selected = []
intial_base_dir_path = os.path.dirname(os.path.realpath(__file__))
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
###########################################################################################################################

###########################################################################################################################

class Application(QMainWindow):
	def __init__(self):
		super().__init__()
		self.buttoncounterbool = 0
		self.base_dir_path = base_dir_path = os.path.dirname(os.path.realpath(__file__))		
		try:
			shutil.rmtree(base_dir_path + '\\tmpDir')
		except:
			pass
		self.sl=[]
		self.size = size = QDesktopWidget().screenGeometry(-1)
		h = size.height()
		w = size.width()
		self.widget_width = w
		rcParams.update({'figure.max_open_warning' : 0})
		rcParams.update({'figure.autolayout': True})
		self.patient = []
		self.h = int(h *.8)		
		self.w = int(w *.8)
		self.create_menu()
		self.edit = 0				
		self.patient_list = [Patient() for i in range(12)]
		self.editlist = []
		self.labels = ['Name', 'Age','Doctor','Hospital', 'Gest. Age', 'Last Period', 'Weight', 'Gender', 'Date']		
		self.def_zscore = []
		self.ratios = Ratios()
		self.setMouseTracking(True)
		self.rint = random.randint(15,65)	
		self.admin = Admin()
		self.failed = []
		self.directorypath = "C:\\"
		self.filedialog = QFileDialog()
		self.tempdir_path = Path(base_dir_path + str('\\tmpDir'))
		os.mkdir('tmpDir')
		self.setDockOptions(QMainWindow.AnimatedDocks)


###########################################################################################################################
#														UI, Widgets
#
#
###########################################################################################################################

	
	def initialwidget(self):
		gboxh = (self.h-50) / 15
		gboxw = self.w / 20
		self.bmheight = bmheight = int((gboxh * 14)/8)
		self.bmwidth = bmwidth = int((gboxw *18)/10)			
		isize = QSize(gboxw,gboxh)
		width = 13
		height = ['A','B','C','D','E','F','G','H']
		self.ind_button = ind_button = [[],[],[],[],[],[],[],[],[],[],[],[]]
		self.p_button = p_button = []
		self.t_button = t_button = [[],[],[],[],[],[],[],[]]
				
		rvwidget = QWidget()
		rvlayout = QVBoxLayout()
		for i in range(len(height)):
			a = QPushButton(height[i])
			a.setSizePolicy(1, QSizePolicy.Expanding)		
			a.setStyleSheet('background-color: #2775bf ; color: white')
			rvlayout.addWidget(a)
			t_button[i].append(a)
		rvlayout.setSpacing(0)	
		rvwidget.setLayout(rvlayout)		

		chwidget = QWidget()
		chlayout = QHBoxLayout()	
		for i in range(width-1):
			a =QPushButton(str(i+1)) 
			a.setSizePolicy(QSizePolicy.Expanding,1)			
			a.setStyleSheet('background-color: #2775bf ; color: white')
			chlayout.addWidget(a)
			p_button.append(a)	
		chlayout.setSpacing(0)			
		chwidget.setLayout(chlayout)	

		bmwidget = QWidget()
		bmlayout = QGridLayout()
		for i in range(len(height)):
			for j in range(1,width):
				a = QPushButton(height[i]+str(j))
				a.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)	
				a.setStyleSheet('background-color: #ffffff')
				a.setCheckable(True)			
				bmlayout.addWidget(a,i,j)
				self.ind_button[j-1].append(a)
				self.t_button[i].append(a)
		
		for i in range(len(self.ind_button)) :
			for x in self.ind_button[i]:
				x.clicked.connect(lambda a, y = x: self.set_initial_widget_button_color(y))

		bmlayout.setSpacing(0)		
		bmwidget.setLayout(bmlayout)

		icon = QLabel()
		pixmap = QPixmap('logo.png')
		iconwidth = pixmap.size().width() * 0.6
		iconheight = pixmap.size().height() * 0.6
		iconpixmap = pixmap.scaled(QSize(iconwidth,iconheight))
		icon.setPixmap(iconpixmap)

		grid_layout = QGridLayout()		
		grid_layout.addWidget(icon,0,0,1,1)	
		grid_layout.addWidget(rvwidget, 1,0,15,1)
		grid_layout.addWidget(chwidget, 0,1,1,20)
		grid_layout.addWidget(bmwidget,1,1,15,20)				
		grid_layout.setSpacing(0)
		iwidget = QWidget()
		iwidget.setLayout(grid_layout)
		self.p_button[0].clicked.connect(lambda: self.patientEditWidget(1, False))
		self.p_button[1].clicked.connect(lambda: self.patientEditWidget(2, False))
		self.p_button[2].clicked.connect(lambda: self.patientEditWidget(3, False))
		self.p_button[3].clicked.connect(lambda: self.patientEditWidget(4, False))
		self.p_button[4].clicked.connect(lambda: self.patientEditWidget(5, False))
		self.p_button[5].clicked.connect(lambda: self.patientEditWidget(6, False))
		self.p_button[6].clicked.connect(lambda: self.patientEditWidget(7, False))
		self.p_button[7].clicked.connect(lambda: self.patientEditWidget(8, False))
		self.p_button[8].clicked.connect(lambda: self.patientEditWidget(9, False))
		self.p_button[9].clicked.connect(lambda: self.patientEditWidget(10, False))
		self.p_button[10].clicked.connect(lambda: self.patientEditWidget(11, False))
		self.p_button[11].clicked.connect(lambda: self.patientEditWidget(12, False))													
		self.setCentralWidget(iwidget)
		self.show()
	
	def set_initial_widget_button_color(self, a):
		for i in range(len(self.ind_button)):
			for x in self.ind_button[i]:
				if a == x:
					count = i
		if a.isChecked():
			a.setStyleSheet('background-color: #0000ff')
			self.patientEditWidget(count, True)
		else:
			a.setStyleSheet('background-color: #ffffff')

	def set_initial_widget_button_color_row(self, a):
		if a.isChecked():
			self.deselect_initial_widget_button_color(a)
			return 
		
		a.setChecked(True)
		if a.isChecked():
			a.setStyleSheet('background-color: #0000ff')
		else:
			a.setStyleSheet('background-color: #ffffff')
	
	def deselect_initial_widget_button_color(self, a):
		a.setChecked(False)
		if a.isChecked():
			a.setStyleSheet('background-color: #0000ff')
		else:
			a.setStyleSheet('background-color: #ffffff')

	def patientEditWidget(self, pid, single):
		try:
			self.rightdock.hide()
		except AttributeError:
			pass
		if single == False :
			for i in self.ind_button[pid-1]:
				self.set_initial_widget_button_color_row(i)

		self.rightdock = QDockWidget()
		rightinput = QWidget()
		rightlayout = QGridLayout()
		patient = self.patient_list[pid-1]
		labellist = [QLabel(self.labels[i]) for i in range(len(self.labels))]
		edits = patient.return_list()
		edits1 = QLineEdit(self)
		edits1.setPlaceholderText(edits[0])
		edits2 = QLineEdit(self)
		edits2.setPlaceholderText(edits[1])
		edits3 = QLineEdit(self)
		edits3.setPlaceholderText(edits[2])
		edits4 = QLineEdit(self)
		edits4.setPlaceholderText(edits[3])
		edits5 = QLineEdit(self)
		edits5.setPlaceholderText(edits[4])
		edits6 = QLineEdit(self)
		edits6.setPlaceholderText(edits[5])
		edits7 = QLineEdit(self)
		edits7.setPlaceholderText(edits[6])
		edits8 = QLineEdit(self)
		edits8.setPlaceholderText(edits[7])
		self.editlist = [edits1,edits2,edits3,edits4,edits5,edits6,edits7,edits8]
		for i in range(len(labellist)):
			rightlayout.addWidget(labellist[i], i, 0,1,1)
		for i in range(len(self.editlist)):
			rightlayout.addWidget(self.editlist[i],i,1,1,2)												
		button = QPushButton('Apply', self)
		self.calendar = QCalendarWidget()
		rightlayout.addWidget(self.calendar, 8, 0, 2, 3)
		rightlayout.addWidget(button, 12, 1, 1, 1)
		rightinput.setLayout(rightlayout)
		button.clicked.connect(lambda: self.update_patient(pid))
		self.rightdock.setWidget(rightinput)
		self.rightdock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.RightDockWidgetArea,self.rightdock)		
		self.show()
	
	def create_menu(self):
		self.menu()
		placeholder = QWidget()
		label = QLabel(placeholder)
		label.setPixmap(QPixmap('Company logo.png'))
		label.setGeometry(100,100, 1500, 750)
		self.top_bar()	
		self.progressbar()				
		self.initialwidget()
		self.statusBar().showMessage('Please Open Data Directory')
		self.show()

	def top_bar(self):
		self.top_bar_dock_widget = QDockWidget()
		placeholder_widget = QWidget()
		grid_layout = QGridLayout()
		self.main_open = QPushButton('&Open', self)
		self.reset = QPushButton('&New Analysis', self)
		self.frequency_view_checkbox = QCheckBox("Frequency")
		blist = [self.main_open, self.reset]
		for i in blist:
			i.setStyleSheet(':enable{background-color: white; color: #2775bf}')
		grid_layout.addWidget(self.main_open, 0, 0)
		grid_layout.addWidget(self.reset, 0, 1)
		grid_layout.addWidget(self.frequency_view_checkbox, 0, 2)
		self.main_open.clicked.connect(self.open_file)
		self.reset.clicked.connect(self.reset_program)
		self.main_open.setEnabled(True)
		self.reset.setEnabled(True)
		placeholder_widget.setLayout(grid_layout)
		grid_layout.setContentsMargins(0,0,0,0)
		self.top_bar_dock_widget.setWidget(placeholder_widget)
		self.top_bar_dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
		for i in blist:
			i.setSizePolicy(QSizePolicy.Expanding,0)	
		placeholder_widget.setSizePolicy(QSizePolicy.Expanding,10)	
		self.addDockWidget(Qt.TopDockWidgetArea, self.top_bar_dock_widget)
		self.show()

	def menu(self):
		self.openAction = openAction = QAction('&Open', self)
		openAction.triggered.connect(self.open_file)
		saveAction = QAction('&Save', self)
		scAction = QAction('&Signifigance Cutoff', self)
		scAction.triggered.connect(lambda:self.setting_popup(ratio = self.ratios))
		exitAction = QAction('&Exit', self)
		exitAction.triggered.connect(qApp.quit)
		aboutAction = QAction('&About', self)
		aboutAction.triggered.connect(self.about_dev)
		saveDirectoryAction = QAction('&Save Directory', self)
		saveDirectoryAction.triggered.connect(self.saveDirectory)
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		settingsMenu = menubar.addMenu('&Settings')		
		aboutMenu = menubar.addMenu('&About')
		fileMenu.addAction(openAction)
		openAction.setEnabled(False)
		aboutMenu.addAction(aboutAction)
		settingsMenu.addAction(scAction)
		settingsMenu.addAction(saveDirectoryAction)
		fileMenu.addAction(exitAction)


	def leftDock(self):
		try:
			self.leftdock.hide()
		except AttributeError:
			pass
		self.dock_widget = QDockWidget()
		placeholder_widget = QWidget()
		grid_layout = QGridLayout()
		patientwidgetlist = self.combine_p_l()
		for i in range(6):
			grid_layout.addWidget(patientwidgetlist[i],i,0)
			grid_layout.setContentsMargins(0,0,0,0)
		for i in range(6,12):
			grid_layout.addWidget(patientwidgetlist[i],i-6,1)
		grid_layout.setSpacing(0)
		grid_layout.setContentsMargins(0,0,0,0)
		placeholder_widget.setLayout(grid_layout)
		self.dock_widget.setWidget(placeholder_widget)
		self.addDockWidget(Qt.LeftDockWidgetArea,self.dock_widget)
		self.dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.dock_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.show()

	def leftDockNew(self):
		try:
			self.leftdock.hide()
		except AttributeError:
			pass			
		self.dock_widget = QDockWidget()
		placeholder_widget = QWidget()
		vBoxLayout = QVBoxLayout()
		buttonList, testList, patientWidget = self.leftDockPatient()
		vBoxLayout.addWidget(patientWidget)
		placeholder_widget.setLayout(vBoxLayout)
		self.dock_widget.setWidget(placeholder_widget)
		self.addDockWidget(Qt.LeftDockWidgetArea,self.dock_widget)
		self.dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.dock_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.show()

	def leftDockPatient(self):
		patientwidget = QWidget()
		patientgrid_layout = QGridLayout()
		patientgrid_layout.setSpacing(20)
		labels = ['Patient 1','Patient 2','Patient 3','Patient 4','Patient 5','Patient 6','Patient 7','Patient 8','Patient 9','Patient 10','Patient 11','Patient 12']
		p1 = QPushButton(labels[0])
		p2 = QPushButton(labels[1])
		p3 = QPushButton(labels[2])
		p4 = QPushButton(labels[3])
		p5 = QPushButton(labels[4])
		p6 = QPushButton(labels[5])
		p7 = QPushButton(labels[6])
		p8 = QPushButton(labels[7])
		p9 = QPushButton(labels[8])
		p10 = QPushButton(labels[9])
		p11 = QPushButton(labels[10])
		p12 = QPushButton(labels[11])
		p1.clicked.connect(lambda: self.show_graph(patient = 1)) 
		p2.clicked.connect(lambda: self.show_graph(patient = 2)) 
		p3.clicked.connect(lambda: self.show_graph(patient = 3)) 
		p4.clicked.connect(lambda: self.show_graph(patient = 4)) 
		p5.clicked.connect(lambda: self.show_graph(patient = 5)) 
		p6.clicked.connect(lambda: self.show_graph(patient = 6))
		p7.clicked.connect(lambda: self.show_graph(patient = 7))
		p8.clicked.connect(lambda: self.show_graph(patient = 8))
		p9.clicked.connect(lambda: self.show_graph(patient = 9))
		p10.clicked.connect(lambda: self.show_graph(patient = 10))
		p11.clicked.connect(lambda: self.show_graph(patient = 11))
		p12.clicked.connect(lambda: self.show_graph(patient = 12))
		buttonList = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]
		for i in range(6):
			patientgrid_layout.addWidget(buttonList[i],i,0)
		for i in range(12):
			patientgrid_layout.addWidget(buttonList[i-6],i,1)
		patientwidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		patientwidget.setLayout(patientgrid_layout)

		failed = []
		testwidget = QWidget()
		testgrid_layout = QGridLayout()
		labels = ['A','B','C','D','E','F','G','H']
		self.cb1 = QCheckBox(labels[0])
		self.cb2 = QCheckBox(labels[1])
		self.cb3 = QCheckBox(labels[2])
		self.cb4 = QCheckBox(labels[3])
		self.cb5 = QCheckBox(labels[4])
		self.cb6 = QCheckBox(labels[5])
		self.cb7 = QCheckBox(labels[6])
		self.cb8 = QCheckBox(labels[7])
		self.checkboxtestList = testList = [self.cb1,self.cb2,self.cb3,self.cb4,self.cb5,self.cb6,self.cb7,self.cb8]

		for i in range(0,4):
			testgrid_layout.addWidget(self.checkboxtestList[i],0,i)
		
		for i in range(4,8):
			testgrid_layout.addWidget(self.checkboxtestList[i],1,i-4)

		testwidget.setLayout(testgrid_layout)

		widget = QWidget()
		vBoxLayout = QVBoxLayout()
		vBoxLayout.setSpacing(10)
		vBoxLayout.addWidget(patientwidget)
		vBoxLayout.addWidget(testwidget)
		widget.setLayout(vBoxLayout)
		return buttonList, self.checkboxtestList, widget	

	def leftDockTest(self):
		failed = []
		widget = QWidget()
		grid_layout = QGridLayout()
		labels = ['A','B','C','D','E','F','G','H']
		cb1 = QCheckBox(labels[0])
		cb2 = QCheckBox(labels[1])
		cb3 = QCheckBox(labels[2])
		cb4 = QCheckBox(labels[3])
		cb5 = QCheckBox(labels[4])
		cb6 = QCheckBox(labels[5])
		cb7 = QCheckBox(labels[6])
		cb8 = QCheckBox(labels[7])
		self.checkboxtestList = testList = [cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8]
		while len(failed) != 0:
			for i in range(len(failed)):
				testList[failed[i]].setStyleSheet('color: red')
			break

		for i in range(0,4):
			grid_layout.addWidget(testList[i],0,i)
		
		for i in range(4,8):
			grid_layout.addWidget(testList[i],1,i-4)

		widget.setLayout(grid_layout)		
		return testList, widget

	def checkboxwidget(self, pid, failed):
		widget = QWidget()
		layout = QGridLayout()
		testA = QCheckBox('A')
		testB = QCheckBox('B')
		testC = QCheckBox('C')
		testD = QCheckBox('D')
		testE = QCheckBox('E')
		testF = QCheckBox('F')
		testG = QCheckBox('G')
		testH = QCheckBox('H')
		tests = [testA, testB, testC, testD, testE, testF, testG, testH]
		while len(failed) != 0:
			for i in range(len(failed)):
				tests[failed[i]].setStyleSheet('color: red')
			break

		for i in range(0,4):
			layout.addWidget(tests[i],0,i)
		
		for i in range(4,8):
			layout.addWidget(tests[i],1,i-4)
		
		widget.setLayout(layout)


		tests.append(pid)
		layout.setSpacing(0)
		return widget, tests		

	def progressbar(self):
		self.qprogressbar = progressbar = QProgressBar()
		self.dock = dock = QDockWidget()
		dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		dock.setWidget(progressbar)
		self.addDockWidget(Qt.BottomDockWidgetArea,dock)

	def centralwidget(self, glist,size):
		try:
			self.uiWidget.hide()
		except:
			pass
		self.setCentralWidget(QLabel("REFRESH"))
		gwidget = QWidget()
		uiWidget =  QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		glayout = QGridLayout()
		glayout.setContentsMargins(0,0,0,0)
		c = 4
		j = 0
		k = 0
		for i in range(size):
			glayout.addWidget(glist[i],j,k)
			k += 1
			if k>= c:
				k = 0
				j += 1
		gwidget.setLayout(glayout)
		layout.addWidget(gwidget,1)
		uiWidget.setLayout(layout)
		uiWidget.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		self.setCentralWidget(uiWidget)
		self.uiWidget = uiWidget
		self.show()

	def label_edit(self,label,edit):
		l = QLabel(label,self)
		e = QLineEdit(edit, self)
		layout = QHBoxLayout()
		layout.addWidget(l)
		layout.addWidget(e)
		widget = QWidget(self)
		widget.setLayout(layout)
		return widget		

	def graphwidget(self, fig, identifier, patient):
		layout = QVBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0,0,0,0)
		pixmap = QPixmap(fig)
		canvas = LabelClickableWidget()
		canvas.setPixmap(pixmap)
		canvas.setScaledContents(True)
		layout.addWidget(canvas)
		gwidget = QWidget()
		gwidget.setLayout(layout)
		canvas.clicked.connect(lambda: self.unselect_reaction(identifier,patient))
		return gwidget
	
	def graphwidget_frequency_view(self,frame):
		# ch1_frame = pd.DataFrame(frame['Ch1 Amplitude'].value_counts())
		# ch2_frame = pd.DataFrame(frame['Ch2 Amplitude'].value_counts())
		# ch1_fig = sb.barplot(data = ch1_frame, x = "Ch1 Amplitude", y = "values")
		# ch2_fig = sb.barplot(data = ch2_frame, x = "Ch2 Amplitude", y = "values")
		# layout = QVBoxLayout()
		# layout.setSpacing(0)
		# layout.setContentsMargins(0,0,0,0)
		# ch1_pixmap = QPixmap(ch1_fig)
		# ch2_pixmap = QPixmap(ch2_fig)
		# canvas1 = FigureCanvas()
		# canvas1.setPixmap(ch1_pixmap)
		# canvas2 = FigureCanvas()
		# canvas2.setPixmap(ch2_pixmap)
		# layout.addWidget(canvas1)
		# layout.addWidget(canvas2)
		# gwidget = QWidget()
		# gwidget.setLayout(layout)
		gwidget = QWidget()
		return gwidget

	def export_dock_widget(self,pid):
		try: 
			self.dock.hide()
		except:
			pass
		try:
			self.rightdock.hide()
		except AttributeError:
			pass
		self.rightdock = QDockWidget()
		rightInfo = QWidget()
		patient_layout = QGridLayout()
		patient = self.patient_list[pid-1]
		labellist = [QLabel(i) for i in self.labels]
		patient = self.patient_list[pid-1]
		patient_info = patient.return_list()
		icon = QLabel()
		icon.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
		pixmap = QPixmap('bg.png')
		iconwidth = pixmap.size().width() * 0.05
		iconheight = pixmap.size().height() * 0.05
		iconpixmap = pixmap.scaled(QSize(iconwidth,iconheight))
		icon.setPixmap(iconpixmap)		
		edits1 = QLabel(self)
		edits1.setText(patient_info[0])
		edits2 = QLabel(self)
		edits2.setText(patient_info[1])
		edits3 = QLabel(self)
		edits3.setText(patient_info[2])
		edits4 = QLabel(self)
		edits4.setText(patient_info[3])
		edits5 = QLabel(self)
		edits5.setText(patient_info[4])
		edits6 = QLabel(self)
		edits6.setText(patient_info[5])
		edits7 = QLabel(self)
		edits7.setText(patient_info[6])
		edits8 = QLabel(self)
		edits8.setText(patient_info[7])
		edits9 = QLabel(self)
		edits9.setText(patient_info[8])
		self.editlist = [edits1,edits2,edits3,edits4,edits5,edits6,edits7,edits8,edits9]
		for i in self.editlist:
			i.setFixedWidth((int(iconwidth)/2))
		for i in range(len(labellist)):
			patient_layout.addWidget(labellist[i], i, 0,1,1)
		for i in range(len(self.editlist)):
			patient_layout.addWidget(self.editlist[i],i,1,1,2)												
		rightInfo.setLayout(patient_layout)
		button_matrix = QWidget()
		bm_layout = QGridLayout()
		view_button = QPushButton('View')
		save_button = QPushButton('Save')
		update_mean_button = QPushButton('Update Mean')
		export_button = QPushButton('Export')
		view_button.clicked.connect(lambda:self.view(pid))
		save_button.clicked.connect(lambda:self.save_patient_info(patient,pid))
		update_mean_button.clicked.connect(lambda:self.setting_popup(ratio = self.ratios))
		export_button.clicked.connect(lambda:self.save_file(patient))
		bm_layout.addWidget(view_button,0,0,1,1)
		bm_layout.addWidget(save_button,0,1,1,1)
		bm_layout.addWidget(update_mean_button,1,0,1,1)
		bm_layout.addWidget(export_button,1,1,1,1)
		bm_layout.addWidget(icon,2,0,2,2)
		button_matrix.setLayout(bm_layout)
		parent_layout = QVBoxLayout()
		parent_layout.addWidget(rightInfo)
		parent_layout.addWidget(button_matrix)
		parent_widget = QWidget()
		parent_widget.setLayout(parent_layout)
		self.rightdock.setWidget(parent_widget)
		self.rightdock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.RightDockWidgetArea,self.rightdock)		
		self.show()

	def reset_program(self):
		try:
			self.removeDockWidget(self.leftdock)
		except AttributeError:
			pass
		try:
			self.removeDockWidget(self.dockwidget)
		except AttributeError:
			pass
		try:	
			self.removeDockWidget(self.dock_widget)
		except AttributeError:
			pass
		try:
			self.removeDockWidget(self.dock)
		except AttributeError:
			pass
		try:
			self.removeDockWidget(self.top_bar_dock_widget)
		except AttributeError:
			pass
		self.setCentralWidget(QWidget())
		self.close()
		shutil.rmtree(self.base_dir_path + '\\tmpDir')
		self.__init__()	

	def unselect_reaction(self,identifier,patient):
		self.checkboxtestList[identifier].setChecked(False)
		if patient == 1:
			self.graph_widget_list1[identifier].hide()
		if patient == 2:
			self.graph_widget_list2[identifier].hide()
		if patient == 3:
			self.graph_widget_list3[identifier].hide()
		if patient == 4:
			self.graph_widget_list4[identifier].hide()
		if patient == 5:
			self.graph_widget_list5[identifier].hide()
		if patient == 6:
			self.graph_widget_list6[identifier].hide()
		if patient == 7:
			self.graph_widget_list7[identifier].hide()
		if patient == 8:
			self.graph_widget_list8[identifier].hide()
		if patient == 9:
			self.graph_widget_list9[identifier].hide()
		if patient == 10:
			self.graph_widget_list10[identifier].hide()
		if patient == 11:
			self.graph_widget_list11[identifier].hide()
		if patient == 12:
			self.graph_widget_list12[identifier].hide()

			

###########################################################################################################################
#															Work Functions
#
#
###########################################################################################################################
	def static_list_file_pattern(self):
		num_list = ["01","02","03","04","05","06","07","08","09","10","11","12"]
		letter_list= ["A","B","C","D","E","F","G","H"]
		file_pattern_list = []
		for i in num_list:
			for x in letter_list:
				file_pattern_list.append(x+i)
		return file_pattern_list

	def open_file(self):
		self.selected_patients = selected_patients = []
		for i in range(len(self.ind_button)):
			for x in range(len(self.ind_button[i])):
				if self.ind_button[i][x].isChecked():
					for p in self.ind_button:
						if self.ind_button[i][x] in p:
							for y in self.t_button:
								if self.ind_button[i][x] in y:
									selected_patients.append(int(i*8) + int(x))
		self.selected_patients_regx_list = selected_patients_regx_list = []
		static_id_list = self.static_list_file_pattern()
		for i in selected_patients:
			selected_patients_regx_list.append(static_id_list[i])
		QCoreApplication.processEvents()
		self.patientname = []
		for i in range(12):
			self.patientname.append('Patient '+str(i+1))
		self.files = files = self.filelist(self.directorypath,selected_patients_regx_list)
		if self.files != None:
			self.work_id_list = self.staticlist()
			self.fl, tempFileLists = self.frame_list()
			try:
				self.work_fullframe = self.fullframe(framelist = self.fl)
			except:
				pass				
			self.qprogressbar.setValue(100)		
			self.dict = self.dictionary(framelist = self.fl, staticlist = selected_patients_regx_list) 
			self.leftDockNew()
			self.reset.setEnabled(True)		
			self.main_open.setEnabled(False)
			self.openAction.setEnabled(False)
			try:
				self.removeDockWidget(self.dock)
			except:
				pass		
			if len(self.failed) != 0 :
				self.post_analysis_popup(False)
			else :
				self.post_analysis_popup(True)
			try:
				self.rightdock.hide()
			except:
				pass

		else:
			print("No files or incorrect file format")


	def progress(self,marker):
		total_length = len(self.files)

		while marker <= total_length:
			self.qprogressbar.setValue(marker)
			if marker == total_length:
				break
			else:
				break

	def saveDirectory(self):
		filedir = QFileDialog.getExistingDirectory(self, "Select Files(s)","C:/")
		self.directorypath = filedir

	def cancel(self):
		dialog = QDialog(QLabel('No file selected!'))
		dialog.show()

	def filelist(self, directory,selected):
		filedir = self.filedialog.getExistingDirectory(None, "Select File(s)", directory)   #'/home/yipeng/analysis')

		if filedir != '':
			filetuple = os.listdir(filedir)
			files = [filedir +'/'+ file for file in filetuple]
		else:
			self.no_file()
			return None			
		self.files_selected_to_open = []
		self.selected_pattern = []
		pattern = self.static_list()
		
		try:
			for i in files:
				for x in selected:
					if re.search(x,i):
						self.files_selected_to_open.append(i)
						self.selected_pattern.append(x)
		except IndexError:
			pass
		try :
			not_selected_files = []
			if len(selected) != len(self.files_selected_to_open):
				for i in self.files_selected_to_open :
					for x in selected:
						if re.search(x,i):
							pass
						else:
							not_selected_files.append(x)
			not_selected_files_string = " " 
			for i in not_selected_files_string :
				not_selected_files_string += i
			if len(not_selected_files) != 0 :
				self.selected_extra_files(not_selected_files_string)
		except :
			pass

		return self.files_selected_to_open


	def load_cluster_graph(self,dataframe,original_frame,labelname, count):
		self.header_list =['Ch1 Amplitude','Ch2 Amplitude']
		graph_title_list = ['A','B','C','D','E','F','G','H']
		try:
			self.scatterplot = sb.lmplot(x=self.header_list[1], y=self.header_list[0], hue = "Cluster", data = dataframe, fit_reg= False, scatter_kws={'s':5},legend = False)
		except TypeError:
			self.scatterplot = sb.lmplot(x=self.header_list[1], y=self.header_list[0], hue = "Cluster", data = original_frame, fit_reg= False, scatter_kws={'s':5},legend = False)			
		self.scatterplot.fig.suptitle(labelname)
		if count < len(self.selected_pattern):
			path_string =  Path(self.selected_pattern[count] +str(".png"))
			cluster_path = Path(self.tempdir_path/path_string)
			self.scatterplot.savefig(str(cluster_path))
		else:
			pass		

	def run_checked(self):
		try:
			cl = self.checked_list()
			idlist = self.checked_frames(cl)
		except:
			return

		pid = int(idlist[-1])
		idlist.pop(-1)
		fl = []
		for i in range(len(idlist)):
			try:
				a = self.dict[idlist[i]]
				fl.append(a)
			except KeyError:
				self.key_error()
		self.selected_frames = fl	

	def tempFileDir(self):
		static_title_pattern = self.static_list_file_pattern()
		lists = []
		graph_title_list = ['A','B','C','D','E','F','G','H']
		for i in range(95):
			test_num = static_title_pattern[i]
			lists.append(str(self.tempdir_path) + str('\\' + test_num )+'.png')
		return lists

	def show_graph(self, patient):
		try:
			self.setWindowState(Qt.WindowMaximized)
			self.dockwidget.close()
			for i in self.checkboxtestList:
				i.setStyleSheet("color: black")
		except:
			pass

		tempFileLists = self.tempFileDir()


		if patient < 10 :
			staticTestList = ["A" + str(0) + str(patient) ,"B" +  str(0) + str(patient) ,"C" +  str(0) + str(patient) , "D" + str(0) + str(patient) ,"E" +  str(0) + str(patient) ,"F" +  str(0) + str(patient) ,"G" +  str(0) + str(patient), "H" + str(0) + str(patient) ]
		else:
			staticTestList = ["A" + str(patient) ,"B" +  str(patient) ,"C" +  str(patient) , "D" + str(patient) ,"E" +  str(patient) ,"F" +  str(patient) ,"G" +  str(patient), "H" + str(patient) ]

		selected_pattern_patient = []
		for i in range(len(staticTestList)):
			for x in self.selected_pattern:
				if re.search(x,staticTestList[i]):
					self.checkboxtestList[i].setChecked(True)
					selected_pattern_patient.append(staticTestList[i])
		for i in range(len(staticTestList)):					
			for x in self.failed :	
				if re.search(x,staticTestList[i]):
					self.checkboxtestList[i].setStyleSheet("color: red")
					self.checkboxtestList[i].setChecked(False)
		tempFileToOpen = []
		for i in selected_pattern_patient:
			for x in tempFileLists:
				if re.search(i,x):
					tempFileToOpen.append(x)

		#TODO need to check the dictionary to fetch which frame to grab. 

		if patient == 1:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list1 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list1) != 0:			
					self.centralwidget(glist = self.graph_widget_list1, size =  len(tempFileToOpen))
				else :
					self.no_file()
			# else:
			# 	selected = self.custom_select_frames(self.selected_pattern)
			# 	self.graph_widget_list1 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
			# 	if len(self.graph_widget_list1) != 0:			
			# 		self.centralwidget(glist = self.graph_widget_list1, size =  len(selected))
			# 	else :
			# 		self.no_file()
			
		if patient == 2:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list2 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list2) != 0:			
					self.centralwidget(glist = self.graph_widget_list1, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list2 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list2) != 0:			
					self.centralwidget(glist = self.graph_widget_list2, size =  len(selected))
				else :
					self.no_file()

		if patient == 3:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list3 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list3) != 0:			
					self.centralwidget(glist = self.graph_widget_list3, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list3 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list3) != 0:			
					self.centralwidget(glist = self.graph_widget_list3, size =  len(selected))
				else :
					self.no_file()

		if patient == 4:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list4 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list4) != 0:			
					self.centralwidget(glist = self.graph_widget_list4, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list4 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list4) != 0:			
					self.centralwidget(glist = self.graph_widget_list4, size =  len(selected))
				else :
					self.no_file()

		if patient == 5:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list5 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list5) != 0:			
					self.centralwidget(glist = self.graph_widget_list5, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list5 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list5) != 0:			
					self.centralwidget(glist = self.graph_widget_list5, size =  len(selected))
				else :
					self.no_file()

		if patient == 6:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list6 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list6) != 0:			
					self.centralwidget(glist = self.graph_widget_list6, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list6 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list6) != 0:			
					self.centralwidget(glist = self.graph_widget_list6, size =  len(selected))
				else :
					self.no_file()

		if patient == 7:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list7 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list7) != 0:			
					self.centralwidget(glist = self.graph_widget_list7, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list7 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list7) != 0:			
					self.centralwidget(glist = self.graph_widget_list7, size =  len(selected))
				else :
					self.no_file()

		if patient == 8:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list8 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list8) != 0:			
					self.centralwidget(glist = self.graph_widget_list8, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list8 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list8) != 0:			
					self.centralwidget(glist = self.graph_widget_list8, size =  len(selected))
				else :
					self.no_file()

		if patient == 9:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list9 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list9) != 0:			
					self.centralwidget(glist = self.graph_widget_list9, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list9 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list9) != 0:			
					self.centralwidget(glist = self.graph_widget_list9, size =  len(selected))
				else :
					self.no_file()

		if patient == 10:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list10 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list10) != 0:			
					self.centralwidget(glist = self.graph_widget_list1, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list10 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list10) != 0:			
					self.centralwidget(glist = self.graph_widget_list10, size =  len(selected))
				else :
					self.no_file()

		if patient == 11:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list11 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list11) != 0:			
					self.centralwidget(glist = self.graph_widget_list11, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list11 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list11) != 0:			
					self.centralwidget(glist = self.graph_widget_list11, size =  len(selected))
				else :
					self.no_file()

		if patient == 12:
			if self.frequency_view_checkbox.isChecked == False:
				self.graph_widget_list12 = [self.graphwidget(tempFileToOpen[i],i,patient) for i in range(len(tempFileToOpen))]
				if len(self.graph_widget_list12) != 0:			
					self.centralwidget(glist = self.graph_widget_list12, size =  len(tempFileToOpen))
				else :
					self.no_file()
			else:
				selected = self.custom_select_frames(self.selected_pattern)
				self.graph_widget_list12 = [self.graphwidget_frequency_view(selected) for i in range(len(selected))]
				if len(self.graph_widget_list12) != 0:			
					self.centralwidget(glist = self.graph_widget_list12, size =  len(selected))
				else :
					self.no_file()
		self.export_dock_widget(patient)

	def checked_frames(self, cl,pid):
		frames = []
		for i in range(len(cl)):
			frames.append(str(pid)+cl[i])
		frames.append(pid)
		return frames	

	def checked_list(self,pid):
		l = ['A','B','C','D','E','F','G','H']
		checked_list = []
		for x in range(0,8):
			if self.checkboxtestList[x].checkState() == 2:
				checked_list.append(l[x])
		return checked_list,pid				

	def checked_patient(self):

		for i in range(len(self.checkboxlist)):
			if self.checkboxlist[i].checkState() == 2:
				return i+1

	def clear_widget(self):

		self.uiWidget.close()

	def save_file(self,patient):
		p_labels = ['Name', 'Age','Doctor','Hospital', 'Gest. Age', 'Last Period', 'Weight', 'Gender', 'Date']
		patient_data = patient.return_data()	
		if patient_data == []:
		 	return self.save_error()			
		patient_info = patient.return_list()
		tid = ['A','B','C','D','E','F','G','H']			
		results = ["FN-1","FN-2","HN"]
		form = '{:<10}|{:<10}\n'
		save_name = patient.return_name()+'AnalysisResults.txt'
		countid = ['C21: ','C18: ','C13: ']
		ratioid = ['R21/18: ','R21/13: ','R18/13: ']
		zscoreid = ['Z21/18: ','Z21/13: ','Z18/13: ']	

		with open(save_name,'w') as output:
			output.write("Report\n\n")
			for i in range(len(p_labels)):
				output.write(str(p_labels[i])+" :")
				output.write(str(patient_info[i])+"\n\n")
				output.write("Results: \n")
			try:
				Z1 = int(patient_data[2][0])
				Z2 = int(patient_data[2][1])
				Z3 = int(patient_data[2][2])
				if Z1 >= 3 and Z2 >=3:
					output.write("Trisomy 21 HIGH RISK \n")
				if Z1 <= -3 and Z3 >= 3:
					output.write("Trisomy 18 HIGH RISK \n")
				if Z2 <= -3 and Z3 <= -3:
					output.write("Trisomy 13 HIGH RISK \n")
				else:
					output.write("LOW RISK")
			except IndexError:
				print('Z SCORE ERROR')
			output.close()

	def combine_p_l (self):
		self.patientlist = patientlist = self.static_patient()
		paitenttitlelist = self.static_labels()
		patientwidgetlist = []
		layoutlist =[]
		for i in range(12):
			patientwidgetlist.append(QWidget())
		for i in range(12):
			layoutlist.append(QVBoxLayout())
		for i in range(len(patientlist)):
			layoutlist[i].addWidget(paitenttitlelist[i])
			layoutlist[i].addWidget(self.patientlist[i][0])
			patientwidgetlist[i].setLayout(layoutlist[i])
		return patientwidgetlist

	def selected(self, state):
		self.sl=[]				
		if state == Qt.Checked:
			self.sl.append(self)


	def set_initial_widget_button_color_with_information(self, a):

		if a.isChecked():
			a.setStyleSheet('background-color: #808080')


	def update_patient(self,pid):
		labels = ['name', 'age','doctor','hospital', 'ges', 'period', 'weight', 'gender', 'date']
		inputs = []
		for i in range(len(self.editlist)):
			inputs.append(self.editlist[i].text())
		date = self.calendar.selectedDate().toString()
		inputs.append(date)
		kwargs = dict(zip(labels,inputs))
		self.patient_list[pid-1].updateValues(**kwargs)	
		for i in range(len(self.ind_button[pid-1])):
			self.ind_button[pid-1][i].setText(inputs[0]+' '+st.ascii_uppercase[i])
			self.ind_button[pid-1][i].setStyleSheet("color: blue")
		for i in self.ind_button[pid-1]:
			self.set_initial_widget_button_color_with_information(i)
		self.rightdock.hide()	

	def refresh_button_name(self, pid):

		self.button_list[pid].setText(self.patient[pid].return_name())		

	def view(self, pid):
		selected = self.custom_select_frames(self.selected_pattern)
		counts, ratios, z_score = self.run_calculations_for_selected_frames(selected)
		self.current_data = data = [counts,ratios,z_score]	
		self.result_popup(data)


	def validate_userandpass(self, user, passw):
		user, passw == 'admin',self.admin.return_password()
		while user and passw != None:
			return 1
		return 0

			
###########################################################################################################################
#												Static Lists
#
#
###########################################################################################################################

	def static_list(self):
		num = ['01','02','03','04','05','06','07','08','09','10','11','12']
		idlist = []
		for i in range(8):
			for x in range(len(num)):
				idlist.append((st.ascii_uppercase[i]+num[x]))
		
		return idlist

	def staticlist(self):
		"Create a Static List of Identifiers"
		pid = ['1','2','3','4','5','6','7','8','9','10','11','12']
		tid = ['A','B','C','D','E','F','G','H']
		lists = []
		for i in range(len(pid)):
			for x in range(len(tid)):
				lists.append(pid[i] + tid[x])
		
		return lists

	def static_labels(self):
		widgetlist = []
		formlist = []
		checkboxlist = []
		patient_name = []
		for i in range(len(self.patient_list)):
			patient_name.append(self.patient_list[i].return_name())		
		self.paitenttitlelist = paitenttitlelist= patient_name
		cb1 = QPushButton(self.patient_list[0].return_name())
		cb2 = QPushButton(self.patient_list[1].return_name())
		cb3 = QPushButton(self.patient_list[2].return_name())
		cb4 = QPushButton(self.patient_list[3].return_name())
		cb5 = QPushButton(self.patient_list[4].return_name())
		cb6 = QPushButton(self.patient_list[5].return_name())
		cb7 = QPushButton(self.patient_list[6].return_name())
		cb8 = QPushButton(self.patient_list[7].return_name())
		cb9 = QPushButton(self.patient_list[8].return_name())
		cb10 = QPushButton(self.patient_list[9].return_name())
		cb11 = QPushButton(self.patient_list[10].return_name())
		cb12 = QPushButton(self.patient_list[11].return_name())
		
		cb1.clicked.connect(lambda: self.show_graph(patient = 1))
		cb2.clicked.connect(lambda: self.show_graph(patient = 2 ))
		cb3.clicked.connect(lambda: self.show_graph(patient = 3))
		cb4.clicked.connect(lambda: self.show_graph(patient = 4))
		cb5.clicked.connect(lambda: self.show_graph(patient = 5))
		cb6.clicked.connect(lambda: self.show_graph(patient = 6))
		cb7.clicked.connect(lambda: self.show_graph(patient = 7))
		cb8.clicked.connect(lambda: self.show_graph(patient = 8))
		cb9.clicked.connect(lambda: self.show_graph(patient = 9))
		cb10.clicked.connect(lambda: self.show_graph(patient =10 ))
		cb11.clicked.connect(lambda: self.show_graph(patient = 11))
		cb12.clicked.connect(lambda: self.show_graph(patient = 12))

		self.checkboxlist = checkboxlist = [cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8,cb9,cb10,cb11,cb12]	
		for i in range(12):
			widgetlist.append(QWidget())
			formlist.append(QFormLayout())
		for i in range(len(checkboxlist)):
			formlist[i].addRow(checkboxlist[i])
			widgetlist[i].setLayout(formlist[i])
		return widgetlist

###########################################################################################################################
#													Calculations
#
#
###########################################################################################################################

	def selected_counts(self, countlist):
		results = [[] for i in range(8)]		
		for i in range(len(countlist)):
			clusters = [[] for y in range(6)]		
			for x in range(len(clusters)):
				clusters[i].append(countlist[i][x])
			results[i].append(clusters)
		return results

	def value_calculation(self, clustercounts):
		total = sum(clustercounts)
		n1813 = sum(clustercounts[:2])
		n18 = sum(clustercounts[:4])
		n21 = clustercounts[0]+clustercounts[2]+clustercounts[4]
		c21 = (np.log(total)-(np.log(n21)))*total
		c18 = (np.log(total)-(np.log(n18)))*total
		c13 = (np.log(total)-(np.log(n1813)))*total
		value_list = [c21, c18, c13]
		return value_list

	def counts_of_c21c18c13(self,counts):
		c21list = []
		c18list = []
		c13list = []
		i = 0
		try:
			while i<len(counts):
				c21list.append(counts[i])
				c18list.append(counts[i+1])
				c13list.append(counts[i+2])
				i+=3
		except IndexError:
				pass
		c21 = sum(c21list)
		c18 = sum(c18list)
		c13 = sum(c13list)
		c21c18c13list = [c21,c18,c13]
		return c21c18c13list

	def ratio_calculation(self, values):
		r2118 = values[0]/values[1]
		r2113 = values[0]/values[2]
		r1813 = values[1]/values[2]
		ratios = [r2118, r2113, r1813]
		return ratios

	def std_dev(self, values):
		s = np.std(values)	
		return s

	def z_score(self, ratio, mean, stdv):
		z_score = ((ratio - mean) / stdv )

		return z_score

	def return_counts(self, framelist):
		counts = []
		for i in range(len(framelist)):
			counts.append([])
		try:
			for i in range(len(framelist)):
				#TODO Sort the list of value counts to conform to the cluster sequence.
				if len((framelist[i]['Cluster'].value_counts().tolist())) > 5 :
					counts[i]= (framelist[i]['Cluster'].value_counts().tolist()) 
		except:
			pass
		return counts		

	def run_calculations_for_selected_frames(self,framelist):
		counts_list = self.return_counts(framelist)
		patient_count_list = []
		refactor_counts_list = []
		ratio_list = []
		stdv_list = []
		mean_list = self.ratios.return_ratio_list()
		z_score_list = []
		total_fn_hn_list = []

		try:
			for i in range(len(counts_list)):
				refactor_counts_list.append(self.value_calculation(counts_list[i]))
			patient_count_list = self.patient_count(refactor_counts_list)

			ratio_list.append(self.ratio_calculation(patient_count_list))
			for i in range(len(ratio_list)):
				stdv_list.append(self.std_dev(ratio_list[i]))
				for x in range(len(ratio_list[i])):
					z_score_list.append(self.z_score(ratio_list[i][x],mean_list[i],stdv_list[i]))
		except IndexError:
			pass
		return patient_count_list, ratio_list, z_score_list

	def patient_count(self,counts_list):
		c21 = []
		c18 = []
		c13 = []
		try:
			for i in range(len(counts_list)):
				c21.append(counts_list[i][0])
				c18.append(counts_list[i][1])
				c13.append(counts_list[i][2])
		except IndexError:
			pass
		return [sum(c21),sum(c18),sum(c13)]

	def save_patient_info(self,patient,pid):
		try:
			patient.set_data(self.current_data)
		except AttributeError:
			selected = self.custom_select_frames(pid)
			counts, ratios, z_score = self.run_calculations_for_selected_frames(selected)
			self.current_data = data = [counts,ratios,z_score]	
			patient.set_data(self.current_data)

###########################################################################################################################
#													Popups
#
#
###########################################################################################################################

	def about_dev(self):
		about_popup = AboutPopup(self)
		about_popup.setGeometry(300,200,400,400)
		about_popup.show()

	def save_error(self):
		text = "Please Press Save Prior to Export"
		about_popup = ErrorPopup(self, text)
		about_popup.setGeometry(300,200,400,200)
		about_popup.show()

	def key_error(self):
		text = 'Selected Key Does Not Exist'
		about_popup = ErrorPopup(self, text)
		about_popup.setGeometry(300,200,400,200)
		about_popup.show()		

	def no_method(self):
		text = 'No Method Selected'
		p = ErrorPopup(self, text)
		p.setGeometry(300,200,400,200)
		p.show()

	def selected_extra_files(self, file_name):
		text = 'Selected Files Does Not Exist' + file_name
		p = ErrorPopup(self, text)
		p.setGeometry(300,200,400,200)
		p.show()

	def no_file(self):
		text = 'No File Opened'
		p = ErrorPopup(self, text)
		p.setGeometry(300,200,400,200)
		p.show()

	def ratioresult(self,ratio):
		p = ResultRatioPopup(self,ratio)
		p.setGeometry(300,200,400,200)
		p.show()

	def result_popup(self,data):
		p = ResultPopup(self,data)
		p.setGeometry(300,200,400,200)
		p.show()

	def graph_popup(self, fig, size):
		g = GraphPopup(self, fig, size)	
		gsize = g.return_size()	
		g.showMaximized()

	def setting_popup(self, ratio):
		s = RatioPopup(self, ratio)
		s.setGeometry(50,50,int(self.w/4),int(self.h/4))
		s.show()


	def calc_popup(self, calc):
		c = CalcPopup(self, calc)
		c.setGeometry(300,200,400,200)
		c.show()

	def post_analysis_popup(self, boolean):
		f = PostAnalysisPopup(self, boolean)
		f.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		f.show()

	def admin_popup(self):
		a = AdminPopup(self,self.admin)
		a.setGeometry(300,200,400,200)
		user, passw = a.return_values()
		self.validate_userandpass(user,passw)
		a.show()

	def mean(self, l):
		return sum(l)/len(l)
		
	def dictionary(self,framelist, staticlist):
		dictionary = dict(zip(staticlist,framelist))
		return dictionary

	def fullframe(self, framelist):
		placeholder=[]
		for i in range(len(framelist)):
			placeholder.append(framelist[i])
		if placeholder == []:
			ds_frame = pd.DataFrame()
		else:
			ds_frame = pd.concat(placeholder, axis = 0, ignore_index = True)
		return ds_frame

	def frame_list(self):
		QCoreApplication.processEvents()
		fl=[]
		gl=[]
		for i in range(len(self.files)):
			QCoreApplication.processEvents()
			frame = self.single_frame(files = self.files[i])
			print('========'+str(i)+'========')	
			for x in self.selected_pattern:
				if re.search(x,self.files[i]):
					label = x
			ds = self.run_analysis(frame = frame, label = label, marker = i)
			gl.append(self.load_cluster_graph(ds,frame,label,i))
			self.progress(i)
			fl.append(ds)
 
		return fl, gl

	def staticlist(self):
		"Create a Static List of Identifiers"
		pid = ['1','2','3','4','5','6','7','8','9','10','11','12']
		tid = ['A','B','C','D','E','F','G','H']
		lists = []
		for i in range(len(pid)):
			for x in range(len(tid)):
				lists.append(pid[i] + tid[x])
		
		return lists

	def single_frame(self,files):
		ds = pd.read_csv(files,index_col = None, header = 0, engine='python')
		return ds

	def frequency_list(self, frame, column, column_num):
		fullframe = frame
		fullframe[column] = (fullframe[column]/100).astype(int)	
		frequency = fullframe.iloc[:,column_num].value_counts().sort_index(ascending = True)	
		# print(len(frequency.index))	
		if len(frequency.index) > 150:
			fullframe = frame
			fullframe[column] = (fullframe[column]/1000).astype(int)	
			frequency = fullframe.iloc[:,column_num].value_counts().sort_index(ascending = True)
		else:
			pass

		frequencylist = self.frequency_to_index(column_num,frequency)
		return frequencylist

	def sequential_values_y(self, frequencylist):
		sequential_values = []		
		print(frequencylist)
		for i in range(len(frequencylist)-1):
			if frequencylist[i+1] - frequencylist[i] > 10:
				sequential_values.append(frequencylist[i]+1)
		return sequential_values

	def sequential_values_x(self, frequencylist):
		sequential_values = []		
		for i in range(len(frequencylist)-1):
			if frequencylist[i+1] - frequencylist[i] > 5:
				sequential_values.append(frequencylist[i]+2)
		return sequential_values	


	def frequency_to_index(self,column_num,frequency):
		ybins = [100,50,10,5,4,1]
		xbins = [50,25,10,5,1]
		bin_results = []	
		if column_num == 0:
			for i in range(len(ybins)):
				sequential_list = self.sequential_values_y(list(frequency[frequency<ybins[i]].index))
				if len(sequential_list) == 2:
					bin_results = sequential_list
					
					
		elif column_num == 1:	
			for i in range(len(xbins)):			
				sequential_list = self.sequential_values_x(list(frequency[frequency>xbins[i]].index))
				if len(sequential_list) == 1:
					bin_results = sequential_list
					
		return bin_results

	def bin_result_filter(self,bin_results):
		return []

	def cluster_configuration(self,values,frame,marker):

		try:
			y_values = values[0]
			x1_values = values[1]
			x2_values = values[2]
			x3_values = values[3] 
			cond1 =((frame['Ch1 Amplitude'] <=(y_values[0]*100))&(frame['Ch2 Amplitude'] < ((x1_values[0]*100)-10)))
			cond3 =((frame['Ch1 Amplitude'] >=((y_values[0]*100)-100))&(frame['Ch1 Amplitude'] < ((y_values[1]*100)-50)))&(frame['Ch2 Amplitude'] < ((x2_values[0]*100)-10))
			cond5 =((frame['Ch1 Amplitude'] >= (((y_values[1]*100)-50))))&(frame['Ch2 Amplitude'] < ((x3_values[0]*100)-10))
			cond2 =((frame['Ch1 Amplitude'] < ((y_values[0]*100)-50))&(frame['Ch2 Amplitude'] >= ((x1_values[0]*100))))
			cond4 =((frame['Ch1 Amplitude'] >= ((y_values[0]*100)-50))&(frame['Ch1 Amplitude'] < ((y_values[1]*100)-50)))&(frame['Ch2 Amplitude'] >= (x2_values[0]*100))
			cond6 =((frame['Ch1 Amplitude'] >= ((y_values[1]*100)-50))&(frame['Ch2 Amplitude'] >= ((x3_values[0]*100))))
			conditions = [cond1,cond2,cond3,cond4,cond5,cond6]
			choices = [1,2,3,4,5,6]
			frame['Cluster'] = np.select(conditions, choices, default = 0)
			countlist = frame['Cluster'].value_counts().tolist()
			try:
				if 	countlist[-1] < (int(sum(countlist)*0.005)):
					frame = frame[frame.Cluster != 0]
			except:
				pass
		except (TypeError,IndexError):
			return frame
		return frame

	def classifyZeroCluster(self, frame, values):
		if frame['Cluster'] == 0:
			if frame['Ch1 Amplitude'] < values[0][0]*100: #1,2
				if frame['Ch2 Amplitude'] >= values[1][0]*100:
					frame['Cluster'] == 2
				else:
					frame['Cluster'] == 1
			elif frame['Ch1 Amplitude'] < values[0][1]*100 and frame['Ch1 Amplitude'] >= values[0][0]*100:  #3,4
				if frame['Ch2 Amplitude'] >= values[2][0]*100:
					frame['Cluster'] == 4
				else:
					frame['Cluster'] == 3
			else:  
				if frame['Ch2 Amplitude'] >= values[3][0]*100:
					frame['Cluster'] == 6
				else:
					frame['Cluster'] == 5
		return frame

	def try_bins(self,frame,axis):
		fullframe = frame
		values = []
		if axis == 'y' :
			values = self.frequency_list(frame = fullframe,column = 'Ch1 Amplitude', column_num = 0)	
		elif axis == 'x':
			values = self.frequency_list(frame = fullframe,column = 'Ch2 Amplitude', column_num = 1)

		return values
		
	def run_analysis(self,frame, label, marker):
		try:
			fullframe = frame.copy()
			y_values = self.try_bins(frame = fullframe, axis = 'y')
			y_values.sort()
			x1_frame = fullframe[frame['Ch1 Amplitude']<=(y_values[0]*100)]
			x2_frame = fullframe[(frame['Ch1 Amplitude']<(y_values[1]*100))&(frame['Ch1 Amplitude']>(y_values[0]*100))]		
			x3_frame = fullframe[frame['Ch1 Amplitude']>=(y_values[1]*100)]		
			x1_values = self.try_bins(frame = x1_frame, axis = 'x')				
			x2_values = self.try_bins(frame = x2_frame, axis = 'x')		
			x3_values = self.try_bins(frame = x3_frame, axis = 'x')			
			values = [y_values,x1_values,x2_values,x3_values]
		except (TypeError, IndexError):
			self.failed.append(label)
			return frame
		
		return self.cluster_configuration(values = values, frame = frame, marker = marker)	

	def cluster_means(self, frame):
		try:
			c5 = frame.loc[frame['Cluster'] == 5]
			c5_h10_mean = c5['Ch1 Amplitude'].nlargest(n = 10, keep='first')
			c6 = frame.loc[frame['Cluster'] == 6]
			c6_h10_mean = c6['Ch1 Amplitude'].nlargest(n = 10, keep='first')
			c2 = frame.loc[frame['Cluster'] == 2]
			c2_h10_mean = c2['Ch2 Amplitude'].nlargest(n = 10, keep='first')
			c4 = frame.loc[frame['Cluster'] == 4]
			c4_h10_mean = c4['Ch2 Amplitude'].nlargest(n = 10, keep='first')
			c6 = frame.loc[frame['Cluster'] == 6]
			c6_h10_mean = c6['Ch2 Amplitude'].nlargest(n = 10, keep='first')
			means = [[c5_h10_mean.mean(),c6_h10_mean.mean()],[c2_h10_mean.mean(),c4_h10_mean.mean(),c6_h10_mean.mean()]]
			return means
		except AttributeError:
			return

	def run_through_frames(self, framelist):
		fail_list = []
		ch1_c5_means = []
		ch1_c6_means = []
		ch2_c2_means = []
		ch2_c4_means = []
		ch2_c6_means = []
		cluster_means_list = []
		for i in range(len(framelist)):
			a = self.cluster_means(framelist[i])
			ch1_c5_means.append(a[0][0])
			ch1_c6_means.append(a[0][1])
			ch2_c2_means.append(a[1][0])
			ch2_c4_means.append(a[1][1])
			ch2_c6_means.append(a[1][2])
			cluster_means_list.append(a)						
		c5_mean_int = self.mean(ch1_c5_means)/100
		c6_mean1_int  = self.mean(ch1_c6_means)/100
		c2_mean_int  = self.mean(ch2_c2_means)/100
		c4_mean_int  = self.mean(ch2_c4_means)/100
		c6_mean2_int  = self.mean(ch2_c6_means)/100
		ints = [c5_mean_int, c6_mean1_int, c2_mean_int, c4_mean_int,c6_mean2_int]

		for i in range(len(cluster_means_list)):
			a = 0		
			if (cluster_means_list[i][0][0]/100) < c5_mean_int:
				a+=1
				if (cluster_means_list[i][0][1]/100) < c6_mean1_int:
					a+=1
					if (cluster_means_list[i][1][0]/100) < c2_mean_int:
						a+=1
						if (cluster_means_list[i][1][1]/100) < c4_mean_int:
							a+=1
							if (cluster_means_list[i][1][2]/100) < c6_mean2_int:
								a+=1
								if a>= 4:
									fail_list.append(i)
		return fail_list

	def failure_detection(self, faillist, staticlist):
		failed = []
		if len(faillist) != 0:
			for i in range(len(faillist)):
				failed.append(staticlist[faillist[i]])
		return failed		

	def custom_select_frames(self,selected_pattern):
		fl = []

		for i in selected_pattern:
			try:
				a = self.dict[i]
				fl.append(a)
			except KeyError:
				self.key_error()
		# print(fl)
		return fl	

###########################################################################################################################
#													Self-Defined Classes
#
#
###########################################################################################################################

class Patient:
	def __init__(self, pid = None):
		self.load_default()
		self.id = pid

	def load_default(self):
		self.name = 'Please Enter Name' 
		self.age = 'Please Enter Age'
		self.weight = 'Please Enter Weight'  
		self.hospital = 'Please Enter Hospital' 
		self.doctor = 'Please Enter Doctor'	
		self.ges = 'Please Enter Gestational Age'
		self.period = 'Please Enter Date of Last Period'
		self.gender = 'Please Enter Gender'	
		self.date = 'Please Select Date'	
		self.id = 0
		self.data = []

	def updateValues(self,**kwargs):
		for key, value in kwargs.items():
			if key == 'name':
				self.name = value
			elif key == 'age':
				self.age = value
			elif key == 'gender':
				self.gender = value
			elif key == 'hospital':
				self.hospital = value
			elif key == 'doctor':
				self.doctor = value
			elif key =='id':
				self.id = value
			elif key == 'ges':
				self.ges = value
			elif key == 'period':
				self.period = value
			elif key == 'date':
				self.date = value
			elif key == 'weight':
				self.weight = value
			elif key == 'data':
				self.data = value

	def printValue(self):
		static = ['Name','Age','Doctor','Hospital','Gestational','Period','Weight','Gender','Date']
		printlist = [self.name, self.age, self.doctor, self.hospital,  self.ges, self.period, self.weight, self.gender, self.date]	
		for i in range(len(printlist)):
			print(static[i]+' : '+printlist[i])

	def return_list(self):
		slist = [self.name, self.age, self.doctor, self.hospital,  self.ges, self.period, self.weight, self.gender, self.date]		
		return slist

	def return_name(self):
		return self.name

	def return_age(self):
		return self.age

	def return_gender(self):
		return self.gender

	def return_hospital(self):
		return self.hospital

	def return_doctor(self):
		return self.doctor

	def return_id(self):
		return self.id

	def return_data(self):
		return self.data

	def set_data(self, data):
		self.data = data

class Ratios:
	def __init__(self):		
		self.load_default()

	def load_default(self):
		self.r1 = 1
		self.r2 = 1
		self.r3 = 1

	def updateValues(self,**kwargs):
		for key, value in kwargs.items():
			if key == 'r1':
				self.r1 = value
			elif key == 'r2':
				self.r2 = value				
			elif key == 'r3':
				self.r3 = value

	def return_ratio_list(self):
		self.ratio_list = [self.r1,self.r2,self.r3]		
		return self.ratio_list

class Admin:
	def __init__(self):
		self.create_admin()

	def create_admin(self):
		self.username = 'admin'
		self.password = 'password'

	def updatePassword(self, password):
		self.password = password

	def validatePassword(self, password):
		while password == self.password:
			return 1
		return 0

	def return_password(self):
		return self.password

	def return_username(self):
		return self.username

	def updateAdmin( self, admin):
		self.admin = admin



###########################################################################################################################
#													PopUp Class
#
#
###########################################################################################################################
class ErrorPopup(QDialog):
	def __init__(self, parent = None, text = None):
		super().__init__(parent)
		self.text = text
		self.body()

	def body(self):
		font = QFont()
		font.setPointSize(16)
		label = QLabel(self.text,self)
		label.setFont(font)
		label.setAlignment(Qt.AlignCenter)
		label.move(40,0)
		button = QPushButton('&Okay!', self)
		button.move(100,70)
		button.clicked.connect(self.close)

class SavePopup(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.body()

	def body(self):
		label = QLabel('Save Complete',self)
		label.setAlignment(Qt.AlignCenter)
		label.move(40,0)
		button = QPushButton('Okay!', self)
		button.move(100,70)
		button.clicked.connect(self.close)		

class ResultRatioPopup(QDialog):
	def __init__(self, parent = None, ratio = None):
		super().__init__(parent)
		self.ratio = ratio
		self.body()

	def body(self):
		font = QFont()
		font.setPointSize(16)
		rounded_ratios = []
		for i in range(len(self.ratio)):
			rounded_ratios.append("{0:.2f}".format(i))
		layout = QGridLayout()
		for i in range(8):
			lbl = QLabel(st.ascii_uppercase[i])
			lbl.setFont(font)
			layout.addWidget(lbl,i+1,0,1,1)		

		labels = ['Test','Ratio1', 'Ratio2', 'Ratio3']
		for i in range(len(labels)):
			lbls = QLabel(labels[i])
			lbls.setFont(font)
			layout.addWidget(lbls,0,i,1,1)
		for i in range(len(rounded_ratios)):
			for y in range(len(rounded_ratios[i])):
				layout.addWidget(QLabel(str(rounded_ratios[i][y])),i+1,y+1,1,1)				

		self.setLayout(layout)



class ResultPopup(QDialog):
	def __init__(self, parent = None, data = None):
		super().__init__(parent)
		self.data = data
		self.body()	

	def body(self):
		font = QFont()
		font.setPointSize(16)
		layout = QGridLayout()
		labels = ['Test Results','Counts 1','Counts 2','Counts 3','Ratios 1','Ratios 2','Ratios 3','Z-Score1', 'Z-Score2', 'Z-Score3']
		for i in range(len(labels)):
			lbl = QLabel(labels[i])
			lbl.setFont(font)
			layout.addWidget(lbl,0,i,1,1)		
		try:
			for i in range(len(self.data[0])):
				num = round(self.data[0][i], 3)
				q = QLabel()
				q.setNum(num)
				q.setFont(font)
				layout.addWidget(q,1,i+1,1,1)
		except IndexError:
			pass
		try:
			for i in range(len(self.data[1][0])):
				num = round(self.data[1][0][i], 3)
				q = QLabel()
				q.setNum(num)
				q.setFont(font)
				layout.addWidget(q,1,i+4,1,1)
		except IndexError:
			pass			
		try:
			for i in range(len(self.data[2])):
				num = round(self.data[2][i], 3)
				q = QLabel()
				q.setNum(num)
				q.setFont(font)
				layout.addWidget(q,1,i+7,1,1)
		except IndexError:
			pass

		self.setLayout(layout)


class AboutPopup(QDialog):

	def __init__(self, parent = None):
		super().__init__(parent)
		self.about()

	def about(self):
		font = QFont()
		font.setPointSize(16)
		layout = QGridLayout()
		label_list = ['Phone Number:  ', 'Email:  ','Mailing Address:  ']
		info_list = ['1-(650)-544-4516', 'info@Atliabiosystems.com', '740 Sierra Vista Ave, Suite E \n Mountain View, CA, 94043']
		labels = [QLabel(i) for i in label_list]
		info = [QLabel(i) for i in info_list]
		icon = QLabel()
		pixmap = QPixmap('bg.png').scaled(100,50)
		icon.setPixmap(pixmap)	
		layout.addWidget(icon,0,0,1,2)	
		for i in range(len(labels)):
			labels[i].setFont(font)
			info[i].setFont(font)
			layout.addWidget(labels[i],i+1,0)
			layout.addWidget(info[i],i+1,1)
		self.setLayout(layout)
	
class GraphPopup(QDialog):
	def __init__(self, parent = None, fig = None, size = None):
		super().__init__(parent)
		self.fig = fig	
		width = float(size.width()/110)
		height = float(size.height()/110)
		self.fig.set_size_inches(width,height)	
		self.body()	

	def body(self):
		layout = QVBoxLayout()
		self.canvas = canvas = FigureCanvas(self.fig)
		canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		canvas.draw()
		canvas.mousePressEvent(self.canvas.close())
		layout.addWidget(canvas)
		self.gwidget = gwidget = QWidget(self)
		gwidget.setLayout(layout)

	def return_size(self):
		w = self.gwidget.width() * 80
		h = self.gwidget.height() * 80
		return [w,h]

	def close(self):
		self.canvas.close()

class RatioPopup(QDialog):
	def __init__(self, parent = None, ratio = None):
		super().__init__(parent)
		self.ratio = ratio
		self.ratio_list = ratio.return_ratio_list()
		self.le = []
		self.body()


	def body(self):
		blayout = QVBoxLayout()	
		font = QFont()
		font.setPointSize(16)
		label = QLabel('Please Insert Means')
		label.setFont(font)
		label.setAlignment(Qt.AlignHCenter)
		labels = ['Mean 21/18', 'Mean 21/13', 'Mean 18/13']
		layout = QGridLayout()
		for i in range(len(labels)):
			lbl = QLabel(labels[i])
			lbl.setFont(font)
			layout.addWidget(lbl,i,0,1,1)
		for i in range(len(self.ratio_list)):
			a = QLineEdit(str(self.ratio_list[i]))
			layout.addWidget(a,i,1,1,1)
			self.le.append(a)
		close_save = QPushButton('Update')
		close_save.clicked.connect(self.update_values)
		layout.addWidget(close_save,4,1,1,1)
		widget = QWidget()
		widget.setLayout(layout)
		blayout.setSpacing(1)
		blayout.addWidget(label)
		blayout.addWidget(widget)
		self.setLayout(blayout)

	def update_values(self):
		inputs = []
		for i in range(len(self.le)):
			inputs.append(self.le[i].text())
		for i in range(len(inputs)):
			inputs[i] = float(inputs[i])
		labels = ['r1','r2','r3']
		kwargs = dict(zip(labels,inputs))
		self.ratio.updateValues(**kwargs)
		self.close()

class GraphWidget(FigureCanvas):
	clicked = pyqtSignal()
	
	def mousePressEvent(self,event):
		if event.button() == Qt.LeftButton:
			self.clicked.emit()
			QWidget.mousePressEvent(self,event)

class LabelClickableWidget(QLabel):
	clicked = pyqtSignal()
	
	def mousePressEvent(self,event):
		if event.button() == Qt.LeftButton:
			self.clicked.emit()
			QWidget.mousePressEvent(self,event)

class CalcPopup(QDialog):
	def __init__(self, parent = None, calc = None):
		super().__init__(parent)
		self.calc = calc
		self.body()

	def body(self):
		label = QLabel('Nothing to Show!',self)
		label.setAlignment(Qt.AlignCenter)
		label.move(40,0)
		button = QPushButton('&Okay!', self)
		button.move(100,70)
		button.clicked.connect(self.close)	

class PostAnalysisPopup(QDialog):
	def __init__(self, parent = None, boolean = None):
		super().__init__(parent)
		self.boolean = boolean
		self.body()

	def body(self):
		if self.boolean:
			layout = QVBoxLayout()
			label = QLabel('All Reactions Succeeded!')
			label.setStyleSheet('color: blue')
			layout.addWidget(label)
			button = QPushButton('Okay', self)
			button.clicked.connect(self.close)
			layout.addWidget(button)
			self.setLayout(layout)

		else:
			layout = QVBoxLayout()
			label = QLabel('Caution! Reaction Failure Detected!')
			label.setStyleSheet('color: red')
			layout.addWidget(label)
			button = QPushButton('Okay', self)
			button.clicked.connect(self.close)
			layout.addWidget(button)
			self.setLayout(layout)
			

	def return_size(self):
		return self.w, self.h


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Application()
	sys.exit(app.exec_())