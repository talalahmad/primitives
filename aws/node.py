#!/usr/bin/python

import web
import sqlite3
import json
from datetime import datetime
from os.path import expanduser

import time
import logging
import requests

#My own scripts
import get
import uploader
#from Log import log
import syslog
import time
import storage

urls = (
	"/", "view_data",
	"/new_user", "new_user",
	"/gateway_receiver","gateway_receiver",
	"/load_tables","load",
	"/marketplace","marketplace",
	"/server","server",
	"/ivr_server","ivr_server",
	"/random_server","random_server",
	"/nexmo_file","nexmo_file",
	"/search_and_get","search_and_get"
	)
mpl = {}
random = {}
# This class contains the information regarding a BTS node. It will tell the node who it is. 
# This will have an IP and port where the node is listening. 
class search_and_get:
	def __init__(self):
		pass
	def GET(self):
		user_data = web.input()
		global random
		if user_data['do'] == 'search':
			#search on aws for a random file uploaded by someone else. For example if you are calling this from rapidcell you can search with my openvpn IP to try and find a file i have uploaded
			result = "";
			if user_data['key'] in random: #is not None:
				#send a non-empty string to the user_data['ip']
				for i in range(0,min(len(random[user_data['key']]),5)):
					result = result+","+random[user_data['key']][i]
			#send result variable back.
			data_to_be_sent = {};
			data_to_be_sent['result'] = result
			data_to_be_sent['ip'] = user_data['ip'] #this is the openvpn ip coming with the request
			data_to_be_sent['id'] = user_data['id']
			thread = get.get('http://128.122.140.120:8080/search_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
			thread.start(); 
		elif user_data['do'] == 'get':
			syslog.syslog("BALU: sending file back %s,%s" %(str(time.time()),user_data['key']))
			filedir = '/home/ec2-user/random' # change this to the directory you want to store the file in.
			filename = user_data['key']
			thread = uploader.file_uploader('http://128.122.140.120:8080/get_handler', '', filedir + '/' + filename)
			thread.start()
			#get a file 

class ivr_server:
	def __init__(self):
		pass
	def POST(self):
		syslog.syslog("BALU: I got something in iver server")
		x = web.input(myfile={})
		filedir = '/home/ec2-user/ivr' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			syslog.syslog("BALU: ivr file:%s at time:%s" %(filename,str(time.time())))
			data_to_be_sent = {};
			data_to_be_sent['ret'] = filename
			data_to_be_sent['app'] = 'IVR'
			thread = get.get('http://128.122.140.120:8080/aws_file_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
			thread.start();
		#raise web.seeother('/upload')


class random_server:
	def __init__(self):
		pass
	def POST(self):
		#syslog.syslog("BALU: I got something in iver server")
		syslog.syslog("BALU: Came to random_server POST")
		x = web.input(myfile={})
		filedir = '/home/ec2-user/random' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			global random;
			if filename.split(':')[1] not in random:
				random[filename.split(':')[1]] = []
			random[filename.split(':')[1]].append(filename)
			syslog.syslog("BALU: time = %s" %str(time.time()))
			syslog.syslog("BALU: random post:%s,%s" %(filename,str(time.time())))
			data_to_be_sent = {};
			data_to_be_sent['ret'] = filename
			data_to_be_sent['app'] = 'SEN'
			thread = get.get('http://128.122.140.120:8080/aws_file_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
			thread.start();
		#raise web.seeother('/upload')


class server:
	def __init__(self):
#		self.name= "central" # this is going to be the small server for the actual implimentation. 
#		mpl = {} # I think this will be the queue containing all the requests 
		pass
	def GET(self):
		global mpl
		#syslog.syslog("BALU: server class invoked")
		user_data=web.input();
		
		identity = user_data['i']
		t = user_data['t']
		d = user_data['d']
		#syslog.syslog("BALU: i = %s, t = %s, d = %s" %(identity,t,d));
		#lets split d over here to 
		d = d.split(","); # fromat is: data(spaced),from_number,from_name,node_name
		from_number = d[1]
		from_name = d[2]
		node_name = d[3]
		d = d[0]
		if t == "MKP":
		#	syslog.syslog("BALU: inside t == MKP")
			if 'sell' in d or 'Sell' in d:
				ret = d+" : "
				#this needs to be put in the queue
				message = d.split(' ') #format sell BALU 5kg 50
				if message[1] not in mpl:
					mpl[message[1]] = []
					mpl[message[1]].append(message[2]+','+message[3])
					
				else:
					mpl[message[1]].append(message[2]+','+message[3])
				syslog.syslog("BALU: post: %f,%s,%s,%s" %(time.time(),identity,t,d));

				data_to_be_sent = {};
				data_to_be_sent['to'] = from_number
				data_to_be_sent['msisdn'] = 767 #this could be problem because it might expect a string
				data_to_be_sent['text'] = ret+"posted"
				thread = get.get('http://'+node_name+'/marketplace_aws_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
				thread.start(); 

			elif 'search' in d or 'Search' in d:
				ret = d+":"
				message = d.split(' ') #format search BALU
				if message[1] in mpl:
					if len(mpl[message[1]]) < 5:
						# for loop till len to compose the message
						for i in range(0,len(mpl[message[1]])):
							temp = mpl[message[1]][i];
							temp = temp.split(',')
							temp = temp[0]+" at "+temp[1]+" per unit,"
							ret = ret+temp
							# send this message back to the node here
					else:
						for i in range(0,5):
							temp = mpl[message[1]][-1*i];
							temp = temp.split(',')
							temp = temp[0]+" at "+temp[1]+" per unit,"
							ret = ret+temp
				else:
					ret = ret+"no such crop found"
					#Done: have to send message back to server, find this code.
					#Done: have to add 767 to the sip_buddies table in the subscriber registry db
					#Done: which db table will tell us from which server this stuff came? I should plug that stuff in here. 
					#Done: testing
					
				data_to_be_sent = {};
				data_to_be_sent['to'] = from_number
				data_to_be_sent['msisdn'] = 767 #this could be problem because it might expect a string
				data_to_be_sent['text'] = ret
				thread = get.get('http://'+node_name+'/marketplace_aws_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
				thread.start(); 
				syslog.syslog("BALU: search: %f,%s,%s,%s" %(time.time(),identity,t,d));

			elif 'buy' in d or 'Buy' in d:
				ret = d+" : "
				message = d.split(' ') #format buy BALU 5KG 52
				if message[1] not in mpl:
					ret = ret+"There is no such crop"
					# then there is nothing to buy
				elif mpl[message[1]] == []:
					ret = ret+"probably sold"
				else:
					search = message[2]+","+message[3]  
					index = -1;
					for i in range(0,len(mpl[message[1]])):
						if mpl[message[1]][i] == search:
							index = i;
							break;

					if index != -1:
						#item was found at index = index
						temp = mpl[message[1]][index].split(',')
						ret = ret+"You bought "+temp[0]+" at "+temp[1]+" per unit"
						#syslog.syslog("index = %d" %index)
						mpl[message[1]].remove(search)

						#could be moved to a transactions folder 
				data_to_be_sent = {};
				data_to_be_sent['to'] = from_number
				data_to_be_sent['msisdn'] = 767 #this could be problem because it might expect a string
				data_to_be_sent['text'] = ret
				thread = get.get('http://'+node_name+'/marketplace_aws_handler','',data_to_be_sent); #node_name coming in each request is the ip of the handler 
				thread.start();
				syslog.syslog("BALU: get: %f,%s,%s,%s" %(time.time(),identity,t,d));
						# for loop from last to first of size 5 to compose message 
		# New user for naming and addressing testing
		elif(t == "NEW"):
			disk_storage = storage.storage()
			output = disk_storage.GET(user_data)
			print output

class node:
	def __init__(self):
		self.name = "my_name"

	def send_data_to_gateway(imsi,name,mode):
		#put in the post request for sending data
		print self.name;

class view_data:
	def __init__(self):
		self.a = 'a';

	def GET(self):
		syslog.syslog("BALU Hello world");
		return 'Hello World';

# this class is used to keep a record of the users in the local node.
# The user data is stored localy in the home directory db called local_db. 
# The table stores TIMESTAMP,IMSI(ID),NAME of the user. 
# Question: In real cellular networks, users have several attributes/service plans/requirements.. how do we compete with that?

class marketplace:
	def __init__(self):
		self.node = node();
		


	def POST(self):
		# import logging
		# logging.basicConfig(format='%(asctime)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s', filename='/var/log/sms-server.log', level=logging.INFO)

		user_data=web.input();
		if len(user_data) is 4:
			syslog.syslog("BALU: user_data has 4 params")
			from_name = user_data['from_name'];
			destination = user_data['destination']
			from_number = user_data['from_number']
			body = user_data['body']
			syslog.syslog("BALU Got SMS: %s" % (body))
			returning = body[::-1]
			data_list = [];
			data_to_be_sent = {}
			data_to_be_sent['to'] = from_number
			data_to_be_sent['msisdn'] = destination
			data_to_be_sent['text'] = returning
			data_list.append(data_to_be_sent)
			thread = get.get('http://128.122.140.120:8080/marketplace_aws_handler','',data_to_be_sent);
			thread.start();
			return "IF was executed"
		else:
			return 'something is wrong'
		'''	if data_list != []:
				logging.info('Inside if')
            # logging.info('Number of data in list %d' % multiple_data_to_send.count)
    			for data in data_list:
        			logging.info('Data %s' % data)             
        			endpoint = 'http://10.8.0.10:8081/nexmo_sms'
        			r = requests.get(endpoint, params=data)
        			data_list.remove(data)
                	# PostHandler.data_sent = {}
        			logging.info('Get response object %s' % r) '''
		

		



class new_user:
	# This constructor is just creating the user data table called LOCAL_USERS in the local_db db. 
	def __init__(self):
		self.node = node();

		self.db_location= expanduser("~")+"/local_db.db";
		server_db = sqlite3.connect(self.db_location);
		cursor=server_db.cursor();
		cursor.execute("CREATE TABLE IF NOT EXISTS LOCAL_USERS (TSTAMP TIMESTAMP, IMSI VARCHAR(16), NAME VARCHAR(16))");
		server_db.close;

	def GET(self):
		user_data=web.input();

		tstamp = datetime.utcnow()
		if len(user_data) is 2:
			imsi = user_data['imsi'];
			name = user_data['name'];
			server_db = sqlite3.connect(self.db_location);
			cursor=server_db.cursor();
			query = "insert into local_users values ('%s','%s','%s');"%(tstamp,imsi,name)
			cursor.execute(query);
			server_db.commit();
			server_db.close;

			#send to gateway node of the current sector 
			node.send_data_to_gateway(imsi,name,"gateway");

			return "data inserted";

		else:
			return "number of parameters is not 2, 'imsi' and 'name' required"



class load:
	def __init__(self):
		self.db_location = expanduser("~")+"/nodes";
		server_db = sqlite3.connect(self.db_location);
		cursor = server_db.cursor();
		cursor.execute("CREATE TABLE IF NOT EXISTS GATEWAYS (NAME VARCHAR(16),ZONE INTEGER)");
		cursor.execute("CREATE TABLE IF NOT EXISTS NODES (NAME VARCHAR(16), GATEWAY VARCHAR(16))");
		
		server_db.close();

	def GET(self):
		gateways = [('gateway1',1),
					('gateway2',2),
					('gateway3',3),
					('gateway4',4),
					('gateway5',5),]

		nodes = [('node1','gateway1'),
				('node2','gateway1'),
				('node3','gateway1'),
				('node4','gateway1'),
				('node5','gateway1'),
				('node6','gateway2'),
				('node7','gateway2'),
				('node8','gateway2'),
				('node9','gateway2'),]

		server_db = sqlite3.connect(self.db_location);
		c = server_db.cursor();
		c.executemany('INSERT INTO GATEWAYS VALUES (?,?)', gateways)
		c.executemany('INSERT INTO NODES VALUES (?,?)',nodes)

		server_db.commit();
		server_db.close();

app = web.application(urls, locals())
if __name__ == "__main__":
	#syslog.openlog(facility=syslog.LOG_LOCAL0);
	syslog.syslog("BALU: Starting web application")
	app.run();



