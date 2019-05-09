import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

global checkPopupAbout, checkPopupSave, checkOpen
checkPopupAbout = False
checkPopupSave = False
checkOpen = False

class Example(QMainWindow):
	def __init__(self):
		super().__init__()
		self.left = 100
		self.top = 200
		self.width = 1080
		self.height = 400
		self.setWindowState(Qt.WindowMaximized)
		self.layout = QVBoxLayout()
		self.create_menu()
		self.load_buttons()
		
	
	def create_menu(self):
		#Actions
		self.openAction = openAction = QAction(QIcon('open.png'), '&Open', self)
		openAction.triggered.connect(self.open_file)
		saveAction = QAction(QIcon('save.png'), '&Save', self)
		saveAction.triggered.connect(self.save_file)
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)
		exitAction.triggered.connect(qApp.quit)
		loadAction = QAction(QIcon('save.png'), '&Load', self)
		loadAction.triggered.connect(self.load_graph)
		aboutAction = QAction('&About', self)
		aboutAction.triggered.connect(self.about_dev)
		
		#Adding Actions
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		aboutMenu = menubar.addMenu('&About')
		fileMenu.addAction(openAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(loadAction)		
		fileMenu.addAction(exitAction)
		aboutMenu.addAction(aboutAction)

		placeholder = QWidget()
		self.statusBar().showMessage('test')
		self.setCentralWidget(placeholder)
		self.show()

	def open_file(self):
		global checkOpen
		filetuple = QFileDialog.getOpenFileNames(self,"Select File(s)",'/home/yipeng/analysis', 'CSV(*.csv)')
		self.files = np.array(list(filetuple[:1])).ravel()
		self.statusBar().showMessage("Opened"+str(filetuple[0]))
		self.read_file()
		self.create_chart()
		checkOpen = True		

	def save_file(self):
		global checkPopupSave
		checkPopupSave = True
		save_name = QFileDialog.getSaveFileName(self, "Save File", '/report'+'.txt')
		self.scatterplot.savefig('ExperimentScatterPlot', format= 'png')
		file = open(save_name[0], 'w')
		file.write("test")
		#file.write(self.ratios)
		file.close()
		save_popup = AboutPopup(self)
		save_popup.setGeometry(300,200,400,200)
		save_popup.show()

	def about_dev(self):
		global checkPopupAbout
		checkPopupAbout = True
		about_popup = AboutPopup(self)
		about_popup.setGeometry(300,200,400,200)
		about_popup.show()

	def read_file(self):
		self.fileName = self.files
		placeholder = []
		for files in self.fileName:
			ds = pd.read_csv(files,index_col = None, header = 0)
			placeholder.append(ds)
		self.ds_frame = pd.concat(placeholder, axis = 0, ignore_index = True)
		ds_cluster = self.ds_frame[self.ds_frame.columns[2]]
		ds_cluster = ds_cluster.values
		self.cluster_num, self.datapoint_count = np.unique(ds_cluster, return_counts = True)
		self.cluster_frequency = np.asarray((self.cluster_num, self.datapoint_count))
		self.total_datapoint = sum(self.datapoint_count)
		self.cnt_gone = self.datapoint_count[0]
		self.cnt_gtwo = self.datapoint_count[1]
		self.cnt_gthree = self.datapoint_count[2]
		self.cnt_gfour = self.datapoint_count[3]
		self.ratios = []
		for x in range(len(self.datapoint_count)):
			self.ratios.append(self.datapoint_count[x]/self.total_datapoint*100)
		meanVal = self.ds_frame.groupby(['Cluster']).mean()
		meanVal = meanVal.add_suffix('_Mean')
		self.mean_list = [meanVal.columns.values.tolist()]+meanVal.values.tolist()

		maxVal = self.ds_frame.groupby(['Cluster']).max()
		maxVal = maxVal.add_suffix('_Max')
		self.max_list = [maxVal.columns.values.tolist()]+maxVal.values.tolist()

		minVal = self.ds_frame.groupby(['Cluster']).min()
		minVal = minVal.add_suffix('_Min')
		self.min_list = [minVal.columns.values.tolist()]+ minVal.values.tolist()
		
		medianVal = self.ds_frame.groupby(['Cluster']).median()
		medianVal = medianVal.add_suffix('_Median')
		self.median_list = [medianVal.columns.values.tolist()]+medianVal.values.tolist()
		
	def load_graph(self):
		self.scatterplot = sb.lmplot(x='Ch1 Amplitude', y='Ch2 Amplitude', data = self.ds_frame, fit_reg= False)
		return self.scatterplot.fig
			
	def create_chart(self):
		self.layout = QVBoxLayout()
		self.tableWidget = QTableWidget()
		self.tableWidget.setColumnCount(11)
		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.setRowCount(5)
		self.tableWidget.setItem(0,0,QTableWidgetItem("Group"))
		self.tableWidget.setItem(0, 1, QTableWidgetItem("Count"))
		self.tableWidget.setItem(0,2,QTableWidgetItem("Ratios"))
		
		for x in self.cluster_frequency[0]:
			for i in range(len(self.cluster_frequency[0])):
				self.tableWidget.setItem(i+1, 0, QTableWidgetItem(str(self.cluster_frequency[0][i])))
				i+=1			
		for x in self.cluster_frequency[1]:
			for i in range(len(self.cluster_frequency[1])):
				self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(self.cluster_frequency[1][i])))
				i+=1
		for x in self.ratios:
			for i in range(len(self.ratios)):
				self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(self.ratios[i])))
				i+=1
		
		self.tableWidget.move(100,100)
		self.layout.addWidget(self.tableWidget)
		self.uiWidget = QWidget()
		self.uiWidget.setAttribute(Qt.WA_DeleteOnClose)
		self.uiWidget.setLayout(self.layout)
		figure = self.load_graph()
		canvas = FigureCanvas(figure)
		canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		canvas.updateGeometry()
		self.layout.addWidget(canvas)
		self.setCentralWidget(self.uiWidget)
		self.show()

	def load_mean(self):
		if checkOpen == True:
			for x in self.mean_list:
				for i in range(len(self.mean_list)):
					self.tableWidget.setItem(i,3,QTableWidgetItem(str(self.mean_list[i][0])))
					self.tableWidget.setItem(i,4,QTableWidgetItem(str(self.mean_list[i][1])))
			self.tableWidget.resizeColumnsToContents()
			self.tableWidget.show()
		else:
			popUp = AboutPopup(self)
			popUp.show()
				
	def load_max(self):
		if checkOpen == True:
			for x in self.max_list:
				for i in range(len(self.mean_list)):
					self.tableWidget.setItem(i,5,QTableWidgetItem(str(self.max_list[i][0])))
					self.tableWidget.setItem(i,6,QTableWidgetItem(str(self.max_list[i][1])))
			self.tableWidget.resizeColumnsToContents()
			self.tableWidget.show()
		else:
			popUp = AboutPopup(self)
			popUp.show()

	def load_min(self):
		if checkOpen == True:
			for x in self.min_list:
				for i in range(len(self.mean_list)):
					self.tableWidget.setItem(i,7,QTableWidgetItem(str(self.min_list[i][0])))
					self.tableWidget.setItem(i,8,QTableWidgetItem(str(self.min_list[i][1])))
			self.tableWidget.resizeColumnsToContents()
			self.tableWidget.show()
		else:
			popUp = AboutPopup(self)
			popUp.show()

	def load_median(self):
		if checkOpen == True:
			for x in self.median_list:
				for i in range(len(self.mean_list)):
					self.tableWidget.setItem(i,9,QTableWidgetItem(str(self.median_list[i][0])))
					self.tableWidget.setItem(i,10,QTableWidgetItem(str(self.median_list[i][1])))
			self.tableWidget.resizeColumnsToContents()
			self.tableWidget.show()
		else:
			popUp = AboutPopup(self)
			popUp.show()


	def load_buttons(self):
		button_widget = QDockWidget()
		multi_widget = QWidget()
		calc1_button = QPushButton('Mean', self)
		calc1_button.setToolTip('Show Mean')
		calc1_button.clicked.connect(self.load_mean)
		calc2_button = QPushButton('Min', self)
		calc2_button.setToolTip('Show Min')
		calc2_button.clicked.connect(self.load_min)
		calc3_button = QPushButton('Max', self)
		calc3_button.setToolTip('Show Max')
		calc3_button.clicked.connect(self.load_max)
		calc4_button = QPushButton('Median', self)
		calc4_button.setToolTip('Show Median')
		calc4_button.clicked.connect(self.load_median)
		calc5_button = QPushButton('Clear', self)
		calc5_button.setToolTip('Clear Widget')
		calc5_button.clicked.connect(self.clear_widget)
		grid = QGridLayout()
		grid.addWidget(calc1_button)
		grid.addWidget(calc2_button)
		grid.addWidget(calc3_button)
		grid.addWidget(calc4_button)
		grid.addWidget(calc5_button)
		multi_widget.setLayout(grid)
		button_widget.setWidget(multi_widget)
		self.addDockWidget(Qt.RightDockWidgetArea,button_widget)
		self.show()

	def clear_widget(self):
		global checkOpen
		self.uiWidget.close()
		checkOpen = False

class AboutPopup(QDialog):

	def __init__(self, parent = None):
		super().__init__(parent)
		if checkPopupAbout == True:
			self.about()
		elif checkPopupSave == True:
			self.save()
		elif checkOpen == False:
			self.error()
		else: 
			print("Cannot popup")

	def about(self):
		about_text = 'App Developed by Neusoft America for _____'
		about_label = QLabel(about_text,self)
		about_label.move(40,0)
		about_label.setAlignment(Qt.AlignCenter)
		close_button = QPushButton('&Close', self)
		close_button.move(100,70)
		close_button.clicked.connect(self.close)

	def save(self):
		save_text = 'Report is Saved!'
		save_label = QLabel(save_text,self)
		save_label.setAlignment(Qt.AlignCenter)
		save_label.move(40,0)
		close_button = QPushButton('&Close', self)
		close_button.move(100,70)
		close_button.clicked.connect(self.close)

	def error(self):
		error_text = 'Error No File Opened!'
		error_label = QLabel(error_text,self)
		error_label.setAlignment(Qt.AlignCenter)
		error_label.move(40,0)
		close_button = QPushButton('&Close', self)
		close_button.move(100,70)
		close_button.clicked.connect(self.close)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())