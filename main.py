#!/usr/bin/env python3
from serialcom import *
from audioengine import *
import logging, queue, sys
from packs import *
from mainwindow import *

try:
	ret = 0
	#logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
	logger = logging.getLogger("BeatDice")
	logger.setLevel(logging.DEBUG)

	pack = SamplePacks()
	pack.load("Dubstep","6x4")
	ser = SerialCom()
	engine = AudioEngine(pack, ser)
	engine.start()

	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow(engine)
	window.show()
	ret = app.exec_()
	engine.close()
	engine.join()
except KeyboardInterrupt:
	engine.close()

sys.exit(ret)
