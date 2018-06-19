#!/usr/bin/env python3
import serial, time

class SerialCom():
	ser = None
	lastGroupValue = [-1,-1,-1,-1,-1,-1,-1,-1]
	syncRequest = b"is111111111111\r\n"
	rcvOn = bytes([0x58, 0x30, 0x31, 0x0D, 0x0A])
	isOpen = False

	rcvMap ={
		b'i001411\r\n':(0, 1),
		b'i001501\r\n':(0, 2),
		b'i001151\r\n':(0, 3),
		b'i001451\r\n':(0, 4),
		b'i001441\r\n':(0, 5),
		b'i001401\r\n':(0, 6),
		b'i001511\r\n':(0, 0),

		b'i005411\r\n':(1, 1),
		b'i005501\r\n':(1, 2),
		b'i005151\r\n':(1, 3),
		b'i005451\r\n':(1, 4),
		b'i005441\r\n':(1, 5),
		b'i005401\r\n':(1, 6),
		b'i005511\r\n':(1, 0),

		b'i011411\r\n':(2, 1),
		b'i011501\r\n':(2, 2),
		b'i011151\r\n':(2, 3),
		b'i011451\r\n':(2, 4),
		b'i011441\r\n':(2, 5),
		b'i011401\r\n':(2, 6),
		b'i011511\r\n':(2, 0),

		b'i041411\r\n':(3, 1),
		b'i041501\r\n':(3, 2),
		b'i041151\r\n':(3, 3),
		b'i041451\r\n':(3, 4),
		b'i041441\r\n':(3, 5),
		b'i041401\r\n':(3, 6),
		b'i041511\r\n':(3, 0),

		b'i101411\r\n':(4, 1),
		b'i101501\r\n':(4, 2),
		b'i101151\r\n':(4, 3),
		b'i101451\r\n':(4, 4),
		b'i101441\r\n':(4, 5),
		b'i101401\r\n':(4, 6),
		b'i101511\r\n':(4, 0),

		b'i015411\r\n':(5, 1),
		b'i015501\r\n':(5, 2),
		b'i015151\r\n':(5, 3),
		b'i015451\r\n':(5, 4),
		b'i015441\r\n':(5, 5),
		b'i015401\r\n':(5, 6), 
		b'i015511\r\n':(5, 0),

		b'i045411\r\n':(6, 1),
		b'i045501\r\n':(6, 2),
		b'i045151\r\n':(6, 3),
		b'i045451\r\n':(6, 4),
		b'i045441\r\n':(6, 5),
		b'i045401\r\n':(6, 6), 
		b'i045511\r\n':(6, 0),

		b'i105411\r\n':(7, 1),
		b'i105501\r\n':(7, 2),
		b'i105151\r\n':(7, 3),
		b'i105451\r\n':(7, 4),
		b'i105441\r\n':(7, 5),
		b'i105401\r\n':(7, 6),
		b'i105511\r\n':(7, 0)
	}


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
		#time.sleep(1)
		#self.ser.write(self.syncRequest)
		#vin = self.ser.readline()
		#while  vin != self.syncRequest:
			#vin = self.ser.readline()
			#time.sleep(0.1)
			#if len(vin)>0: print(vin)
		#time.sleep(1)
		vin = self.ser.readline()
		#print(vin)
		loop = -1
		group = -1
		if len(vin)>0:
			if vin in self.rcvMap:
				group, loop = self.rcvMap[vin]

			if self.lastGroupValue[group] == loop:
				return [-1,-1]
			self.lastGroupValue[group] = loop
			if group>-1 and loop>-1: print(group, loop)
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
		


