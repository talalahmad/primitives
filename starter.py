import get 
import syslog
import time

## configuration setting 
user_number = 0;
myself = "http://128.122.140.115:8080/little_server"
### fill this as per experiment 
how_many = 100;

def make_new_user():
	global user_number;
	global myself
	print "New user request came"
	user_id = user_number;
	user_number = user_number+1;
	#If new user then t is NEW and i is the identity on my machine and you have to issue a global identity, myself is the machine it is coming from 
	data_to_be_sent = {}
	data_to_be_sent['i'] = user_id;
	data_to_be_sent['t'] = "NEW";
	data_to_be_sent['d'] = "something"+","+str(user_id)+","+str(user_id)+","+myself;

	syslog.syslog("AALU: uid=%s and time=%s" %(user_id,str(time.time())))
	thread = get.get('http://ec2-52-29-11-132.eu-central-1.compute.amazonaws.com:8080/server','',data_to_be_sent);
#	thread = get.get('http://0.0.0.0:8081/server','',data_to_be_sent);
	thread.start();
#	thread.join();



for i in range(0,how_many):
	make_new_user();