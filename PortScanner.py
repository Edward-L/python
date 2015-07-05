# -*- coding: utf-8 -*-
import threading
import socket
import sys
import os
import cmd
import Queue

#port 
PortList = [21,22,23,25,80,135,137,139,445,1433,1502,3306,3389,8080]

#get Queue
def GetQueue(list):
	PortQueue = Queue.Queue(65535)
	for p in list:
		PortQueue.put(p)
	return PortQueue

#the threading numuber of scan
nThread = 20

#threading lock
lock = threading.Lock()

#Timeout 
Timeout = 3.0

#OpenPort
OpenPort = []

class ScanThread(threading.Thread):
	def __init__(self, scanIP):
		threading.Thread.__init__(self)
		self.IP = scanIP


	def Ping(self,Port):
	 	global OpenPort, lock, Timeout
	 	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 	sock.settimeout(Timeout)
	 	address = (self.IP, Port)
	 	try:
	 		sock.connect(address)
	 	except:
	 		sock.close()
	 		return False
		sock.close()
		OpenPort.append(Port)
		if lock.acquire():
			print "IP:%s  Port:%d" % (self.IP, Port)
			lock.release()
		return True

class ScanThreadSingle(ScanThread):
	def __init__(self, scanIP, SingleQueue):
		ScanThread.__init__( self, scanIP)
		self.SingleQueue = SingleQueue

	def run(self):
		while not self.SingleQueue.empty():
			p = self.SingleQueue.get()
			self.Ping(p)
tudou.c 

class ScanThreadMulti(ScanThread):
	def __init__(self, scanIP, PortList):
		ScanThread.__init__( self, scanIP)
		self.List = PortList[:]

	def run(self):
		for p in self.List:
			self.Ping(p)

class Shell(cmd.Cmd):
	u'''
 	 ____            _     ____
	|  _ \ ___  _ __| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __
	| |_) / _ \| '__| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
	|  __/ (_) | |  | |_   ___) | (_| (_| | | | | | | |  __/ |
	|_|   \___/|_|   \__| |____/ \___\__,_|_| |_|_| |_|\___|_|

											by Edward_L
    port [port..] set the port you want to scan 
        default：21, 22, 23, 25, 80, 135, 137, 139, 445, 1433, 1502, 3306, 3389, 8080
        example：port 21,23,25
        example: port 1000..2000
        example: port 80,443,1000..1500
    scan [IP] IP adress you want to scan
        example: scan 192.168.1.5
    search [IP begin]-[IP end] 
        example: search 192.168.1.1-192.168.1.100
    time [timeout] set timeout default 3 
        example: time 5
    cls clear the screen
    listport print the PortList
    help open help
        '''
	def __init__(self):
		cmd.Cmd.__init__(self)
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.prompt = "Port Scan >>"
		self.intro = "welcome !!!"

	def do_EOF(self):
   	    return True

	def do_help(self, line):
   	    print self.__doc__

#set port
	def do_port(self, line):
   	    global PortList
   	    PortList = []
   	    ListTmp = line.split(',')
   	    for port in ListTmp:
   			if port.find("..") < 0:
				if not port.isdigit():
					print "wrong port!!"
    				return False
				PortList.append(int(port))
			else:
				RangeList = port.split("..")
				if not (RangeList[0].isdiglit() and RangeList[1].isdiglit()):
					raise ValueError
    				exit()
    			for i in range(int(RangeList[0]),int(RangeList[1])):
    				PortList.append(i)

	def do_scan(self, line):
		global nThread, PortList
		ThreadList = []
		strIP = line
		SingleQueue = GetQueue(PortList)
		for i in range(0, nThread):
			t = ScanThreadSingle(strIP, SingleQueue)
			ThreadList.append(t)
		for t in ThreadList:
			t.start()
		for t in ThreadList:
			t.join()	

	def do_search(self, line):
		global nThread, PortList
		ThreadList = []
		(BeginIP,EndIP) = line.split("-")
		try:
			socket.inet_aton(BeginIP)
			socket.inet_aton(EndIP)
		except:
			print "wrong!!!"
			return
		IPRange = BeginIP[0:BeginIP.rfind('.')]
		begin = BeginIP[BeginIP.rfind('.') + 1:]
		end = EndIP[EndIP.rfind('.') + 1:]
		for i in range(int(begin),int(end)):
			strIP = "%s.%s" %(IPRange, i)
			t = ScanThreadMulti(strIP, PortList)
 			ThreadList.append(t)
		for t in ThreadList:
			t.start()
		for t in ThreadList:
			t.join()

	def do_listport(slef, line):
		global PortList
		for p in PortList:
			print p,
		print '\n'

	def do_time(self, line):
		global Timeout
		try:
			Timeout = float(line)
		except:
			print u"wrong!!!"

	def do_cls(slef, line):
		os.system("clear")

if '__main__' == __name__:
	try:
		os.system("clear")
		shell = Shell()
		shell.cmdloop()
	except:
		exit()