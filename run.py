import os, sys, re, time, traceback, serial, tty, json, termios, fcntl, httplib2
fd = sys.stdin.fileno()

ser = None
#os.system('clear')

run=1

def initSerial():
	global ser

	try:
		ser.close()
	except:
		pass

	ser = serial.Serial("/dev/ttyAMA0", 9600)

def cleanSerial():
	global ser

	try:
		ser.close()
	except:
		pass

def normaliseSerialData(serialData):
	out = ''

	for c in serialData:
		out = out + str(ord(c))

	return out

def pullFromFirebase():
	http = httplib2.Http()
	url = 'https://intense-heat-9265.firebaseio.com/visitors.json'
	response, content = http.request(url)
	return content

def pushToFirebase(jsonDataStr, headers={}):
	http = httplib2.Http()
	url = 'https://intense-heat-9265.firebaseio.com/visitors.json'
	response, content = http.request(url, 'PUT', body=jsonDataStr, headers=headers)
	#print response
	#print content

def cleanStringForFirebase(val):
	val = val.replace('.', '_')
	val = val.replace('@', '__')
	return val

def registerRfidTag(email, rfidToken):
	data = pullFromFirebase()
	#data = json.loads(data)

	print '---'
	print data
	print '---'
	time.sleep(2)

	#json = '{"' + email + '" : {"name" : "' + str(rfidToken) + '"}}'
	email = cleanStringForFirebase(email)
	json = '{"' + email + '" : {"rfid" : "' + str(rfidToken) + '"}}'

	try:
		print 'Registering...'
		pushToFirebase(json)
	except:
		print 'Failed.'
		pass
	finally:
		time.sleep(2)
		displayScreen('menu')

def getKeyPress():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return ch

#def getKeyPress():
#	oldterm = termios.tcgetattr(fd)
#	newattr = termios.tcgetattr(fd)
#	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
#	termios.tcsetattr(fd, termios.TCSANOW, newattr)
#
#	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
#	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
#
#	try:
#		return sys.stdin.read(1)
#	except IOError:
#		pass

def displayScreen(screen):
	title = 'ITT078 - RFID'

	os.system('clear')
	print title
	print '=============='

	if screen == 'menu':
		print 'Choose an action:'
		print '[1] - Register user'
		print '[2] - Emulate product stand'
		print '[3] - Test RFID reader'
		print '[4] - Dump firebase'
		print '[q] - QUIT'

	elif screen == 'register':
		controlLoopRegister()
	elif screen == 'emulate':
		controlLoopEmulate()
	elif screen == 'test':
		controlLoopTest()
	elif screen == 'dumpfirebase':
		controlLoopDumpFirebase()

def controlLoopDumpFirebase():
	json = pullFromFirebase()
	print json
	time.sleep(5)
	displayScreen('menu')

def controlLoopRegister():
	email = raw_input("Enter email address:")
	
	try:
		rfidToken = readRFID()

		if rfidToken:
			print ("RFID token: %s" % rfidToken)
			registerRfidTag(email=email, rfidToken=rfidToken)
	except:
		print 'Failed.'
		pass
	finally:
		time.sleep(2)
		displayScreen('menu')

def controlLoopEmulate():
	print 'Hold RFID tag over sensor...'

def controlLoopTest():
	print 'Hold RFID tag over sensor...'

	try:
		rfidToken = readRFID()
		print ("RFID token: %s" % rfidToken)
	except:
		print 'Failed.'
		pass
	finally:
		time.sleep(2)
		displayScreen('menu')

def readRFID():
	stop = False

	initSerial()

	while not stop:
		try:
			read = ''
			read = ser.readline()
			read = read.strip()
			read = normaliseSerialData(read)

		except serial.serialutil.SerialException:
			initSerial()
			pass
		except:
			cleanSerial()
			print sys.exc_info()
			print traceback.format_exc()
			stop = True
		finally:
			if not read == '':
				cleanSerial()
				return read

# init
stop = False
displayScreen('menu')

initSerial()
#print ser

# control loop
while not stop:
	char = getKeyPress()

	if char == '1':
		displayScreen('register')
	elif char == '2':
		displayScreen('emulate')
	elif char == '3':
		displayScreen('test')
	elif char == '4':
		displayScreen('dumpfirebase')
	elif char == 'q':
		print 'Quitting...'
		stop = True

#ser.close()

#termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
#fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

print 'end'
