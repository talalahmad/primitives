import get 
import syslog
import time
import threading 
import multiprocessing
from aws import storage
import urllib2
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

class bts_client2:
	def __init__(self,user_number, myself, how_many):
		self.how_many = how_many;
		self.myself=myself
		self.start_number = user_number

	def rip(self):
		disk_storage = storage.storage()

		for i in range(0,self.how_many):
			from_number = self.start_number+i;
		#	print from_number;
			from_name = from_number;
			node_name = self.myself;
			t="NEW"
			output = disk_storage.store(from_number,from_name,node_name,t)
			if output is True:
				#have to send back a response saying that i have saved something. 
				syslog.syslog("BALU: True returned")
				syslog.syslog("BALU: uid=%s and time=%s" %(from_number,str(time.time())))
			elif output is False:
				syslog.syslog("BALU: False returned")
				syslog.syslog("BALU: uid=%s and time=%s" %(from_number,str(time.time())))


class bts_client3:
	def __init__(self,user_number, myself, how_many):
		self.how_many = how_many;
		self.myself=myself
		self.start_number = user_number

	def rip(self):
		disk_storage = storage.storage()

		for i in range(0,self.how_many):
			from_number = self.start_number+i;
			print from_number;
			from_name = from_number;
			node_name = self.myself;
			t="NEW"

			x = int(from_number)%10
			if x == 1:
				node = 8090
			elif x ==2:
				node = 8091
			elif x ==3:
				node = 8092
			elif x ==4:
				node = 8093
			elif x ==5:
				node = 8094
			elif x ==6:
				node = 8095
			elif x ==7:
				node = 8096
			elif x ==8:
				node = 8097
			elif x ==9:
				node = 8098
			else:
				node = 8099
			
			print node;
		# 	data_to_be_sent = {}
		# 	data_to_be_sent['i'] = identity;
		# 	data_to_be_sent['t'] = "NEW";
		# 	data_to_be_sent['d'] = user_data['d'];
		# #	syslog.syslog("BALU: uid=%s and time=%s" %(identity,str(time.time())))
		# 	thread = get.get('http://127.0.0.1:'+str(node)+'/server','',data_to_be_sent);
		# 	thread.start();
		# 	syslog.syslog("BALU: Node selected is %s" %node);



port = 8080
bts_process = []
syslog.syslog("AALU: starter starting here here here")
# for i in range(0,5):
# 	bts_process.append('')
# for i in range(0,5):
# 	bts_process[i] = bts_client(user_number+(i*1000000000), myself+str(port+i)+myself2, 500);
# 	bts_process[i].start();
# for i in range(0,5):
# 	bts_process[i].join();

print time.time()
a = bts_client2(100000000000,myself,500)
a.rip();
print time.time()


#a = bts_client3(100000000000,myself,1)
#a.rip();