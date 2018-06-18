#!/usr/bin/env python3
import threading, time, os, logging, json, pygame, queue
from packs import *

class AudioEngine(threading.Thread):
	lock = threading.Lock()
	pack = None
	samples = []
	logger = logging.getLogger("AudioEngine")
	bpm = 140
	abort = False
	timer = None
	bpmCounter = 0
	q = queue.Queue()
	currentSample = [-1,-1,-1,-1,-1,-1,-1,-1]
	queuedSample  = [-1,-1,-1,-1,-1,-1,-1,-1]
	serial = None
	serialInputEnabled = True

	# --------------------------------------------------------------------------------
	def __init__(self, pack=None, serial=None): 
		threading.Thread.__init__(self) 
		self.logger.setLevel(logging.DEBUG)
		self.serial = serial
		pygame.mixer.init()
		pygame.mixer.set_num_channels(8) 
		self.setPack(pack)

	# --------------------------------------------------------------------------------
	def __del__(self):
		if self.timer is not None:
			self.timer.cancel()

	# --------------------------------------------------------------------------------
	def serialEnabled(self, enabled):
		self.serialInputEnabled = enabled

	# --------------------------------------------------------------------------------
	def getPack(self):
		return self.pack

	# --------------------------------------------------------------------------------
	def getCurrentBeat(self):
		return self.bpmCounter
	# --------------------------------------------------------------------------------
	def setPack(self,pack):
		if pack is None:
			return
		if self.timer is not None:
			self.timer.cancel()
		self.pack    = pack
		self.samples = self.pack.samples
		self.bpm     = self.pack.bpm

		self.timer = threading.Timer(60.0/float(self.bpm), self.startSamples)
		self.timer.start()
	
	# --------------------------------------------------------------------------------
	def getQueued(self):
		return self.queuedSample

	# --------------------------------------------------------------------------------
	def getCurrent(self):
		return self.currentSample

	# --------------------------------------------------------------------------------
	def close(self):
		self.abort = True
		if self.timer is not None:
			self.timer.cancel()

	# --------------------------------------------------------------------------------
	def play(self, grp, idx):
		if self.pack is None:
			return
		if grp < len(self.samples):
			i = 0
			if idx > 0 and idx <= len(self.samples[grp]) and self.samples[grp][idx-1] is not None and self.currentSample[grp] != idx:
				i = idx
			self.q.put([grp, i])
			self.queuedSample[grp] = i

	# --------------------------------------------------------------------------------
	def stop(self, grp):
		if self.pack is None:
			return
		if grp < len(self.samples):
			self.q.put([grp, 0])
			self.queuedSample[grp] = 0

	# --------------------------------------------------------------------------------
	def startSamples(self):
		if self.pack is None:
			return
		
		self.bpmCounter = 0 if self.bpmCounter==3 else self.bpmCounter+1
		self.timer = threading.Timer(60.0/float(self.bpm), self.startSamples)
		if not self.abort:
			self.timer.start()

		if self.bpmCounter == 0:
			if not self.q.empty():
				print("start")
				while not self.q.empty():
					grp, idx = self.q.get_nowait()

					if self.currentSample[grp] != idx:
						self.currentSample[grp] = idx
						pygame.mixer.Channel(grp).stop()
						if idx > 0:
							print("  ", self.samples[grp][idx-1]["displayName"])
							pygame.mixer.Channel(grp).play(pygame.mixer.Sound(self.samples[grp][idx-1]["name"]), loops=-1)
				self.q.task_done()

	# --------------------------------------------------------------------------------
	def run(self):
		while not self.abort:
			if self.serialInputEnabled:
				group, loop = self.serial.read()
				if loop >= 0 and group >= 0:
					self.play(group, loop)
			else:
				time.sleep(1)

