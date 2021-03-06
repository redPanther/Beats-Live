#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui,QtWidgets,uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
	engine = None
	showQueued = True
	currentOld = [99,99,99,99,99,99,99,99]
	pad_list = {}
	#pad_color_list = [
		#['#ff5858','#593134', '#7f3434'],
		#['#ff8a60','#593e37', '#7f523a'],
		#['#ffdf6f','#59533a', '#7f7344'],
		#['#77ed87','#35573e', '#46784f'],
		#['#45ebfc','#28565e', '#142b2f'],
		#['#ff8fb9','#583e4c', '#7f4f61'],
		#['#ba9ee6','#453f58', '#302b42'],
		#['#6cb5f7','#304860', '#3a73a0']
	#]

	# --------------------------------------------------------------------------------
	def __init__(self, engine):
		super(MainWindow,self).__init__()

		self.engine = engine
		self.ui = uic.loadUi('mainwindow.ui', self)
		self.showNormal()
		
		self.ui.cbPacks.clear()
		for p in self.engine.getPack().getPacks():
			self.ui.cbPacks.addItem(p[0]+" "+p[1])
		self.ui.cbPacks.setCurrentText(self.engine.getPack().packName +" "+self.engine.getPack().pv)
		print(self.engine.getPack().packName +" "+self.engine.getPack().pv)
		listOfPushButtons = QtCore.QObject.findChildren(self.ui.frame_pads, QPushButton )
		for obj in listOfPushButtons:
			objName = str(obj.objectName())
			if objName.startswith("bt"):
				self.pad_list[objName] = obj
				obj.clicked.connect(self.btnClicked)
				group = int(objName[2])
				loop  = int(objName[4])

		self.engine.registerBeatsCounter(self.onBeatChanged)
		self.engine.registerSampleChanged(self.tick)
		self.onPackLoad()

	# --------------------------------------------------------------------------------
	def onPackLoad(self):
		for btnName in self.pad_list:
			if btnName.startswith("bt"):
				group = int(btnName[2])
				loop  = int(btnName[4])

				if group < len(self.engine.samples) and loop < len(self.engine.samples[group]):
					self.pad_list[btnName].setText(self.engine.samples[group][loop]["displayName"].replace(" ","\n"))
				else:
					self.pad_list[btnName].setText("")

	# --------------------------------------------------------------------------------
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

	# --------------------------------------------------------------------------------
	def onBeatChanged(self, currentBeat):
		self.ui.beatRadio1.setChecked(currentBeat == 0)
		self.ui.beatRadio2.setChecked(currentBeat == 1)
		self.ui.beatRadio3.setChecked(currentBeat == 2)
		self.ui.beatRadio4.setChecked(currentBeat == 3)

	# --------------------------------------------------------------------------------
	def tick(self):
		current = self.engine.getCurrent()
		queued = self.engine.getQueued()
		if current is None or len(current) == 0:
			return
		self.showQueued = not self.showQueued and queued is not None and len(queued)>0


		for group, loop in enumerate(current):
			#print(group, loop, self.currentOld[group])
			if group>=0 and loop>=0:
				for idx in range(6):
					if idx != loop-1:
						self.pad_list['bt'+str(group)+'_'+str(idx)].setChecked(False)
				if loop > 0:
					self.pad_list['bt'+str(group)+'_'+str(loop-1)].setChecked(True)
		self.currentOld = current

		#print(queued)
		#if self.showQueued:
			#for group, loop in enumerate(queued):
				#if group>=0 and loop>0:
					#self.pad_list['bt'+str(group)+'_'+str(loop-1)].setStyleSheet('color: #ffffff;background-color: %s;' % (self.pad_color_list[group][0]))

	# --------------------------------------------------------------------------------
	@pyqtSlot()
	def packChanged(self):
		current = self.ui.cbPacks.currentText()
		idx = current.rfind(" ")
		packName    = current[:idx]
		packVariant = current[idx+1:]
		
		pack = self.engine.getPack()
		if (pack.packName + " " + pack.pv) != current:
			print("load", current)
			self.engine.stop()
			for btnName in self.pad_list:
				self.pad_list[btnName].setChecked(False)
			pack.load(packName, packVariant)
			self.engine.setPack(pack)
			self.onPackLoad()

