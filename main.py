#!/usr/bin/env python3
from serialcom import *
from audioengine import *
import logging, queue, sys
from packs import *

try:
	ret = 0
	#logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
	logger = logging.getLogger("BeatsLive")
	logger.setLevel(logging.DEBUG)

	packName = "DJ Vadim"
	packSize = "6x4"
	packDir  = "packs"
	
	if len(sys.argv)>1: packDir  = sys.argv[1]
	if len(sys.argv)>2: packName = sys.argv[2]
	if len(sys.argv)>3: packSize = sys.argv[3]
	pack = SamplePacks(packDir)
	pack.load(packName, packSize)
	ser = SerialCom()
	engine = AudioEngine(pack, ser)
	engine.start()

	if len(sys.argv) <= 2:
		from mainwindow import *

		app = QtWidgets.QApplication(sys.argv)
		window = MainWindow(engine)
		window.show()
		ret = app.exec_()
		engine.close()
	engine.join()
except KeyboardInterrupt:
	pass

engine.close()
sys.exit(ret)
