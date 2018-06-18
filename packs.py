#!/usr/bin/env python3

import os, logging, json

class SamplePacks:
	pack = None
	packDir = None
	packName = ""
	pv = ""
	samples = []
	logger = logging.getLogger("SamplePacks")
	bpm = 140

	# --------------------------------------------------------------------------------
	def __init__(self,packDir = "packs"):
		self.packDir = packDir

	# --------------------------------------------------------------------------------
	def getGridSize(self):
		return [len(self.samples), 0 if len(self.samples) == 0 else len(self.samples[0])]

	# --------------------------------------------------------------------------------
	def getPackName(self):
		return [self.packName, self.pv]

	# --------------------------------------------------------------------------------
	def getPacks(self):
		ret = []
		if os.path.isdir(self.packDir):
			for d in [name for name in os.listdir(self.packDir) if os.path.isdir(os.path.join(self.packDir, name))]:
				for s in ("6x4", "8x4"):
					if os.path.exists(self.packDir+"/"+d+"/"+s+".json"):
						ret.append((d,s,))

		return ret

	# --------------------------------------------------------------------------------
	def load(self,packName, s):
		self.packName = packName
		self.pv = s
		self.samples.clear()

		try:
			p = self.packDir+"/"+self.packName
			with open(p+'/'+self.pv+'.json') as json_data:
				d = json.load(json_data)
				for i in d["grids"][0]["pads"]:
					grp = int(i["col"])
					idx = int(i["line"])
					snd = str(i["sampleName"])
					if os.path.exists(p+'/samples/'+snd):
						self.logger.info( "load %s %s %s" % (grp, idx, snd))
						while grp > len(self.samples)-1:
							self.samples.append([])
						#while grp > len(self.currentSample)-1:
						#	self.currentSample.append(0)
						while idx > len(self.samples[grp])-1:
							self.samples[grp].append(None)
						
						sd = None
						with open(p+'/samples/'+os.path.splitext(os.path.basename(snd))[0]+".json") as json_data_snd:
							sd = json.load(json_data_snd)
							#print(sd)
						self.samples[grp][idx] = sd
						self.samples[grp][idx]['name'] = p+'/samples/'+self.samples[grp][idx]['name']
						self.bpm = self.samples[grp][idx]['bpm']

		except Exception as e:
			self.logger.error("error while loading sample pack (%s)" % (str(e)) )
			self.samples.clear()

if __name__ == '__main__':
	p = SamplePacks()

	print(p.getPacks())
