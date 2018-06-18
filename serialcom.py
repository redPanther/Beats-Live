#!/usr/bin/env python3
import serial, time

class SerialCom():
	ser = None
	lastGroupValue = [-1,-1,-1,-1,-1,-1,-1,-1]
	syncRequests = [b"is111111111111\r\n", b"is11111111110F\r\n", b"is11111111101F\r\n", b"is111111111F00\r\n", b"is111111111F11\r\n", b"is111111111001\r\n", b"is111111111FFF\r\n", b"is1111111110F0\r\n"]
	rcvOn = bytes([0x58, 0x30, 0x31, 0x0D, 0x0A])
	isOpen = False

	# --------------------------------------------------------------------------------
	def __init__(self):
		try:
			self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400,timeout=0,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

			if self.ser is None:
				raise
			if not self.ser.isOpen():
				self.ser.open()
			time.sleep(2)
		
			self.ser.write(self.rcvOn)
			time.sleep(2)
			self.isOpen = self.ser.isOpen()
		except Exception as e:
			self.isOpen = False
			print("serial CUL-Stick interface disabled", str(e))
		
	# --------------------------------------------------------------------------------
	def close(self):
		if self.ser.isOpen():
			self.ser.close()

	# --------------------------------------------------------------------------------
	def isOpen(self):
		return self.isOpen and self.ser.isOpen()

	# --------------------------------------------------------------------------------
	def read(self):
		if not self.isOpen or not self.ser.isOpen():
			return [-1, -1]

		for sr in self.syncRequests:
			print(">",sr)
			self.ser.write(sr)
			vin = ""
			while self.ser.readline() != sr:
				time.sleep(0.1)
			vin = self.ser.readline()
			print(vin)
			loop = -1
			group = -1
			if len(vin)>0:
				#print(vin)
				if   vin == b'i001411\r\n': loop = 1; group = 0
				elif vin == b'i001501\r\n': loop = 2; group = 0
				elif vin == b'i001151\r\n': loop = 3; group = 0
				elif vin == b'i001451\r\n': loop = 4; group = 0
				elif vin == b'i001441\r\n': loop = 5; group = 0
				elif vin == b'i001401\r\n': loop = 6; group = 0
				elif vin == b'i001511\r\n': loop = 0; group = 0

				elif vin == b'i005411\r\n': loop = 1; group = 1
				elif vin == b'i005501\r\n': loop = 2; group = 1
				elif vin == b'i005151\r\n': loop = 3; group = 1
				elif vin == b'i005451\r\n': loop = 4; group = 1
				elif vin == b'i005441\r\n': loop = 5; group = 1
				elif vin == b'i005401\r\n': loop = 6; group = 1
				elif vin == b'i005511\r\n': loop = 0; group = 1

				elif vin == b'i011411\r\n': loop = 1; group = 2
				elif vin == b'i011501\r\n': loop = 2; group = 2
				elif vin == b'i011151\r\n': loop = 3; group = 2
				elif vin == b'i011451\r\n': loop = 4; group = 2
				elif vin == b'i011441\r\n': loop = 5; group = 2
				elif vin == b'i011401\r\n': loop = 6; group = 2
				elif vin == b'i011511\r\n': loop = 0; group = 2

				elif vin == b'i041411\r\n': loop = 1; group = 3
				elif vin == b'i041501\r\n': loop = 2; group = 3
				elif vin == b'i041151\r\n': loop = 3; group = 3
				elif vin == b'i041451\r\n': loop = 4; group = 3
				elif vin == b'i041441\r\n': loop = 5; group = 3
				elif vin == b'i041401\r\n': loop = 6; group = 3
				elif vin == b'i041511\r\n': loop = 0; group = 3

				elif vin == b'i101411\r\n': loop = 1; group = 4
				elif vin == b'i101501\r\n': loop = 2; group = 4
				elif vin == b'i101151\r\n': loop = 3; group = 4
				elif vin == b'i101451\r\n': loop = 4; group = 4
				elif vin == b'i101441\r\n': loop = 5; group = 4
				elif vin == b'i101401\r\n': loop = 6; group = 4
				elif vin == b'i101511\r\n': loop = 0; group = 4

				elif vin == b'i015411\r\n': loop = 1; group = 5
				elif vin == b'i015501\r\n': loop = 2; group = 5
				elif vin == b'i015151\r\n': loop = 3; group = 5
				elif vin == b'i015451\r\n': loop = 4; group = 5
				elif vin == b'i015441\r\n': loop = 5; group = 5
				elif vin == b'i015401\r\n': loop = 6; group = 5 
				elif vin == b'i015511\r\n': loop = 0; group = 5

				elif vin == b'i045411\r\n': loop = 1; group = 6
				elif vin == b'i045501\r\n': loop = 2; group = 6
				elif vin == b'i045151\r\n': loop = 3; group = 6
				elif vin == b'i045451\r\n': loop = 4; group = 6
				elif vin == b'i045441\r\n': loop = 5; group = 6
				elif vin == b'i045401\r\n': loop = 6; group = 6 
				elif vin == b'i045511\r\n': loop = 0; group = 6

				elif vin == b'i105411\r\n': loop = 1; group = 7
				elif vin == b'i105501\r\n': loop = 2; group = 7
				elif vin == b'i105151\r\n': loop = 3; group = 7
				elif vin == b'i105451\r\n': loop = 4; group = 7
				elif vin == b'i105441\r\n': loop = 5; group = 7
				elif vin == b'i105401\r\n': loop = 6; group = 7
				elif vin == b'i105511\r\n': loop = 0; group = 7

				#if self.lastGroupValue[group] == loop:
				#	return [-1,-1]
				#self.lastGroupValue[group] = loop
				if group>-1 and loop>-1:
					print(group, loop)
		return [group, loop]


# --------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		ser = SerialCom()

		while True:
			g, l = ser.read()
			time.sleep(0.5)
			if g>=0 and l>=0:
				print(g,l)

	except KeyboardInterrupt:
		ser.close()
		


