#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui,QtWidgets,uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
	t      = None
	engine = None
	showQueued = True
	currentOld = [99,99,99,99,99,99,99,99]
	pad_list = {}
	pad_color_list = [
		['#ff5858','#593134', '#7f3434'],
		['#ff8a60','#593e37', '#7f523a'],
		['#ffdf6f','#59533a', '#7f7344'],
		['#77ed87','#35573e', '#46784f'],
		['#45ebfc','#28565e', '#142b2f'],
		['#ff8fb9','#583e4c', '#7f4f61'],
		['#ba9ee6','#453f58', '#302b42'],
		['#6cb5f7','#304860', '#3a73a0']
	]

	def __init__(self, engine):
		super(MainWindow,self).__init__()
		self.engine = engine
		self.ui = uic.loadUi('mainwindow.ui', self)
		self.showNormal()
		
		listOfPushButtons = QtCore.QObject.findChildren(self.ui.frame_pads, QPushButton )
		for obj in listOfPushButtons:
			if str(obj.objectName()).startswith("bt"):
				self.pad_list[str(obj.objectName())] = obj
				obj.clicked.connect(self.btnClicked)
				
		self.t = QtCore.QTimer()
		self.t.setSingleShot(False)
		self.t.timeout.connect(self.tick)
		self.t.start(1000)
		
		
	def btnClicked(self,checked=False):
		obj = self.sender()
		objName = str(obj.objectName())
		if objName.startswith("bt"):
			group = int(objName[2])
			loop  = int(objName[4])
			if checked:
				self.engine.play(group, loop+1)
			else:
				self.engine.stop(group)
		
	def tick(self):
		current = self.engine.getCurrent()
		currentBeat = self.engine.getCurrentBeat()
		queued = self.engine.getQueued()
		self.showQueued = not self.showQueued

		self.ui.beatRadio1.setChecked(currentBeat == 0)
		self.ui.beatRadio2.setChecked(currentBeat == 1)
		self.ui.beatRadio3.setChecked(currentBeat == 2)
		self.ui.beatRadio4.setChecked(currentBeat == 3)

		for group, loop in enumerate(current):
			#print(group, loop, self.currentOld[group])
			if group>=0 and loop>=0:
				for idx in range(6):
					if idx != loop-1:
						self.pad_list['bt'+str(group)+'_'+str(idx)].setChecked(False)
						self.pad_list['bt'+str(group)+'_'+str(idx)].setStyleSheet('color: #000000;background-color: %s;' % (self.pad_color_list[group][1]))
				if loop > 0:
					self.pad_list['bt'+str(group)+'_'+str(loop-1)].setChecked(True)
					self.pad_list['bt'+str(group)+'_'+str(loop-1)].setStyleSheet('color: #ffffff;background-color: %s;' % (self.pad_color_list[group][0]))
		self.currentOld = current

		#print(queued)
		if self.showQueued:
			for group, loop in enumerate(queued):
				if group>=0 and loop>0:
					self.pad_list['bt'+str(group)+'_'+str(loop-1)].setStyleSheet('color: #ffffff;background-color: %s;' % (self.pad_color_list[group][0]))

		



