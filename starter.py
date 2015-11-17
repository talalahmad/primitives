import get 
import syslog
import time
import threading 
import multiprocessing

## configuration settings
### fill this as per experiment  
user_number = 1000000000;
myself = "http://127.0.0.1:"
myself2 = "/little_server"
how_many = 1000;

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


port = 8080
bts_process = []
syslog.syslog("AALU: starter starting here here here")
for i in range(0,5):
	bts_process.append('')
for i in range(0,5):
	bts_process[i] = bts_client(user_number+(i*1000000000), myself+str(port+i)+myself2, 10);
	bts_process[i].start();
for i in range(0,5):
	bts_process[i].join();
