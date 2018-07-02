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
	callback_beats = None
	callback_sample = None

	# --------------------------------------------------------------------------------
	def __init__(self, pack=None, serial=None): 
		threading.Thread.__init__(self) 
		self.logger.setLevel(logging.DEBUG)
		self.serial = serial
		pygame.mixer.pre_init(44100, 16, 2, 4096) 
		pygame.mixer.init()
		pygame.mixer.set_num_channels(8)
		self.setPack(pack)

	# --------------------------------------------------------------------------------
	def __del__(self):
		if self.timer is not None:
			self.timer.cancel()

	def registerBeatsCounter(self,callback_beats=None):
		self.callback_beats = callback_beats

	def registerSampleChanged(self,callback_sample=None):
		self.callback_sample = callback_sample

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
		self.stop()
		if self.timer is not None:
			self.timer.cancel()
		self.pack    = pack
		self.samples = self.pack.samples
		self.bpm     = self.pack.bpm

		for grp,v in enumerate(self.samples):
			for idx, vv in enumerate(self.samples[grp]):
				self.samples[grp][idx]["sound"] = pygame.mixer.Sound(self.samples[grp][idx]["name"])
				gain = float(self.samples[grp][idx-1]["pad"]["gain"])
				if gain < 1.0:
					self.samples[grp][idx]["sound"].set_volume(gain)

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
	def stop(self, grp=-1):
		if self.pack is None:
			return
		if grp < 0:
			for grp in range(len(self.queuedSample)):
				self.q.put([grp,0])
				self.queuedSample[grp] = 0
			pygame.mixer.stop()
		elif grp < len(self.samples):
			self.q.put([grp, 0])
			self.queuedSample[grp] = 0

	# --------------------------------------------------------------------------------
	def startSamples(self):
		try:
			if self.pack is None:
				return
		
			self.bpmCounter = 0 if self.bpmCounter==3 else self.bpmCounter+1
			self.timer = threading.Timer(60.0/float(self.bpm), self.startSamples)
			if not self.abort:
				self.timer.start()

			if self.callback_beats is not None:
				self.callback_beats(self.bpmCounter)
			if self.bpmCounter == 0:
				if not self.q.empty():
					print("start")
					while not self.q.empty():
						grp, idx = self.q.get_nowait()

						if grp < len(self.currentSample) and self.currentSample[grp] != idx:
							self.currentSample[grp] = idx
							pygame.mixer.Channel(grp).stop()
							if idx > 0 and os.path.exists(self.samples[grp][idx-1]["name"]):
								print("  ", self.samples[grp][idx-1]["displayName"]) # ,self.samples[grp][idx-1]["pad"]["gain"]
								pygame.mixer.Channel(grp).play(self.samples[grp][idx-1]["sound"], loops=-1)

					self.q.task_done()
					if self.callback_sample is not None:
						self.callback_sample()
		except Exception as e:
			print("startSamples", e)

	# --------------------------------------------------------------------------------
	def run(self):
		while not self.abort:
			if self.serialInputEnabled:
				group, loop = self.serial.read()
				if loop >= 0 and group >= 0:
					self.play(group, loop)
			else:
				time.sleep(1)

