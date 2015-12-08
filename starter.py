import get 
import syslog
import time
import threading 
import multiprocessing
from aws import storage
import urllib2
import sys 
import myssh

## configuration settings
### fill this as per experiment  
user_number = 1000000000;
myself = "http://127.0.0.1:"
myself2 = "/little_server"
how_many = 1000;

#nodes=["172.31.47.90","172.31.8.192","172.31.1.241","172.31.17.5","172.31.4.150","172.31.6.20","172.31.27.49","172.31.14.204","172.31.0.223","172.31.10.69"]
nodes = ["52.18.192.127","54.208.21.58","54.152.146.161","52.34.77.143","52.53.251.110","52.77.238.23","52.192.211.194","52.62.0.165","54.233.132.14","52.28.22.121"]
keys=["ireland.pem","virginia.pem","virginia.pem","oregon.pem","california.pem","singapore.pem","tokyo.pem","sydney.pem","saopaulo.pem","frankfurt.pem"]

def make_new_users(user_number, myself, how_many):
	# global user_number;
	# global myself
	#print "New user request came"
	thread = [];
	for i in range(0,how_many):
		thread.append('')
	for i in range(0,how_many):		
		user_id = user_number;
		user_number = user_number+1;
		#If new user then t is NEW and i is the identity on my machine and you have to issue a global identity, myself is the machine it is coming from 
		
		data_to_be_sent = {}
		data_to_be_sent['i'] = user_id;
		data_to_be_sent['t'] = "NEW HASH";
		data_to_be_sent['d'] = "something"+","+str(user_id)+","+str(user_id)+","+myself;

		syslog.syslog("AALU: uid=%s and time=%s" %(user_id,str(time.time())))
		thread[i] = get.get('http://127.0.0.1:8090/server','',data_to_be_sent);
	#	thread = get.get('http://0.0.0.0:8081/server','',data_to_be_sent);
		print i
		thread[i].start();
	#	thread.join();
	for i in range(0,how_many):
		thread[i].join()

class bts_client(multiprocessing.Process):
	def __init__(self, user_number, myself, how_many):
		multiprocessing.Process.__init__(self)
		self.user_number = user_number;
		self.myself = myself;
		self.how_many = how_many; 

	def run(self):
		make_new_users(self.user_number, self.myself, self.how_many);

class bts_client2:
	def __init__(self,user_number, myself, how_many):
		self.how_many = how_many;
		self.myself=myself
		self.start_number = user_number

	def rip(self):
		disk_storage = storage.storage()
		disk_storage.clean();

		for i in range(0,self.how_many):
			from_number = self.start_number+i;
		#	print from_number;
			from_name = from_number;
			node_name = self.myself;
			t="NEW"
			output = disk_storage.store(from_number,from_name,node_name,t)
			if output is True:
				#have to send back a response saying that i have saved something. 
				syslog.syslog("BALU: uid=%s and time=%s" %(from_number,str(time.time())))
			elif output is False:
				syslog.syslog("BALU: uid=%s and time=%s" %(from_number,str(time.time())))


class bts_client3:
	def __init__(self,user_number, myself, how_many):
		self.how_many = how_many;
		self.myself=myself
		self.start_number = user_number

	def clean(self):
		for i in range(0,10):
			data_to_be_sent = {}
		 	data_to_be_sent['i'] = "a";
		 	data_to_be_sent['t'] = "CLEAN";
		 	data_to_be_sent['d'] = 'd,d,d,d,d';
		 	thread = get.get('http://'+nodes[i]+':8080/server','',data_to_be_sent);
		 	thread.start();
		 	thread.join();
		 	syslog.syslog("BALU: Just cleaned node:%s" %nodes[i]);

	def rip(self):
		for i in range(0,len(nodes)-1):
			myssh.connect_before(nodes[i],keys[i],self.how_many)

		disk_storage = storage.storage()
		self.clean();
		thread = []

		for i in range(0,self.how_many):
			from_number = self.start_number+i;
			print from_number;
			from_name = from_number;
			node_name = self.myself;
			t="NEW"

			x = int(from_number)%10
			if x == 1:
				node = nodes[1]
			elif x ==2:
				node = nodes[2]
			elif x ==3:
				node = nodes[3]
			elif x ==4:
				node = nodes[4]
			elif x ==5:
				node = nodes[5]
			elif x ==6:
				node = nodes[6]
			elif x ==7:
				node = nodes[7]
			elif x ==8:
				node = nodes[8]
			elif x ==9:
				node = nodes[9]
			else:
				node = nodes[0]
			print node;

		 	data_to_be_sent = {}
		 	data_to_be_sent['i'] = from_name;
		 	data_to_be_sent['t'] = "NEW";
		 	from_number = str(from_number)
		 	data_to_be_sent['d'] = from_number+","+from_number+","+from_number+","+from_number;
			syslog.syslog("BALU: uid=%s and time=%s" %(from_name,str(time.time())))
			try:
		 		thread.append(get.get('http://'+node+':8080/server','',data_to_be_sent));
		 		thread[-1].start();
		 	except IndexError:
		 		print "there was an indexError"
		 	syslog.syslog("BALU: Node selected is %s" %node);
		for i in range(0,self.how_many):
			thread[i].join()

		for i in range(0,len(nodes)-1):
			myssh.connect_after(nodes[i],keys[i],self.how_many)



port = 8080
bts_process = []
syslog.syslog("BALU: starter starting here here here")
# for i in range(0,5):
# 	bts_process.append('')
# for i in range(0,5):
# 	bts_process[i] = bts_client(user_number+(i*1000000000), myself+str(port+i)+myself2, 500);
# 	bts_process[i].start();
# for i in range(0,5):
# 	bts_process[i].join();

# number = sys.argv[1]
# print time.time()
# syslog.syslog("BALU: Number of users=%s Starting time=%s" %(number,str(time.time())))
# a = bts_client2(100000000000,myself,int(number))
# a.rip();
# syslog.syslog("BALU: Number of users=%s Ending time=%s" %(number,str(time.time())))
# print time.time()



number = sys.argv[1]
print time.time()
syslog.syslog("BALU: Number of users=%s Starting time=%s" %(number,str(time.time())))
a = bts_client3(100000000000,myself,int(number))
a.rip();
syslog.syslog("BALU: Number of users=%s Ending time=%s" %(number,str(time.time())))
print time.time()