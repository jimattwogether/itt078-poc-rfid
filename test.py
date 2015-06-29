import os, serial
ser = serial.Serial("/dev/ttyAMA0", 9600)

try:
	os.system('clear')
	print 'RFID data:'
	print '=========='

	while 1==1:
		read = ser.readline()
		read = read.strip()

		if not read == '':
			print read

		read = ''
except:
	ser.close()

ser.close()
