#!/usr/bin/python

import web
import sqlite3
import json
from datetime import datetime
from os.path import expanduser
import hash
import time
import logging
import requests

urls = (
	"/", "view_data",
	"/new_user", "new_user",
	"/gateway_receiver","gateway_receiver",
	"/load_tables","load",
	"/marketplace","marketplace"
	)

# This class contains the information regarding a BTS node. It will tell the node who it is. 
# This will have an IP and port where the node is listening. 
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
		return 'Hello World';

# this class is used to keep a record of the users in the local node.
# The user data is stored localy in the home directory db called local_db. 
# The table stores TIMESTAMP,IMSI(ID),NAME of the user. 
# Question: In real cellular networks, users have several attributes/service plans/requirements.. how do we compete with that?

class marketplace:
	def __init__(self):
		self.node = node();
		loglvl=logging.DEBUG;
		logging.basicConfig(format=('%(asctime)s %(module)s %(funcName)s '
                                    '%(lineno)d %(levelname)s %(message)s'),
                            filename='/var/log/marketplace.log',level=loglvl)

	def POST(self):
		user_data=web.input();
		if len(user_data) is 4:
			from_name = user_data['from_name'];
			destination = user_data['destination']
			from_number = user_data['from_number']
			body = user_data['body']
			logging.info("Got SMS: %s" % (body))
			returning = body[::-1]
			data_list = [];
			data_to_be_sent = {}
			data_to_be_sent['to'] = from_number
			data_to_be_sent['msisdn'] = destination
			data_to_be_sent['text'] = returning
			data_list.append(data_to_be_sent)

			if data_list != []:
				logging.info('Inside if')
            # logging.info('Number of data in list %d' % multiple_data_to_send.count)
    			for data in data_list:
        			logging.info('Data %s' % data)             
        			endpoint = 'http://10.8.0.10:8081/nexmo_sms'
        			r = requests.get(endpoint, params=data)
        			data_list.remove(data)
                	# PostHandler.data_sent = {}
        			logging.info('Get response object %s' % r)
		else:
			return 'something is wrong'

		



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

class gateway_receiver:
	def __init__(self, name):
		self.node = node();
		self.db_location = expanduser("~")+"/gateway.db";
		self.name = name;
		self.hash = hash.Hash(self.get_gateways);
		server_db = sqlite3.connect(self.db_location);
		cursor = server_db.cursor();
		cursor.execute("CREATE TABLE IF NOT EXISTS ZONE_USERS (TSTAMP TIMESTAMP, IMSI VARCHAR(16), NAME VARCHAR(16), BTS VARCHAR(max), RESOLVER VARCHAR(max))");
		cursor.execute("CREATE TABLE IF NOT EXISTS RESOLVED (TSTAMP TIMESTAMP, IMSI VARCHAR(16), NAME VARCHAR(16), BTS VARCHAR(max), GATEWAY VARCHAR(max))");

		server_db.commit();
		server_db.close();

	def GET(self):
		user_data= web.input();

		if len(user_data) is 4: #message is coming from one of the BTS nodes in zone
			if user_data['mode'] == 'gateway':
				imsi = user_data['imsi'];
				name = user_data['name'];
				node = user_data['node'];
				#check if it already exists or not

				if self.already_exists(imsi,name) is False:
					
					tstamp = datetime.utcnow();
					resolver = self.hash.get_node(user_data['imsi']);
					
					#add to zone_users
					server_db = sqlite3.connect(self.db_location);
					cursor = server_db.cursor();
					cursor.execute("insert into zone_users values(?,?,?,?,?)",(tstamp,imsi,name,node,resolver));

					#send it to resolver
					self.node.send_data_to_gateway(imsi,name,"resolver");

				else:
					return "user already exists in zone_users";
			else:
				return "invalid mode";

		elif len(user_data) is 5: # message is coming from a gateway node 
			if user_data['mode'] == 'resolver':
				#add to resolved
				tstamp = datetime.utcnow();
				imsi = user_data['imsi'];
				name = user_data['name'];
				node = user_data['node'];
				gateway = user_data['gateway'];

				server_db = sqlite3.connect(self.db_location);
				cursor= server_db.cursor();
				cursor.execute("insert into resolved values(?,?,?,?,?)",(tstamp,imsi,name,node,gateway));
				server_db.commit();
				server_db.close();
				return "user added to the resolver's records"

			else:
				return "invalid mode"
		else:
			return "number of parameters is not 3 or 5, 'imsi' and 'name' and 'mode' required"

	def already_exists(self, imsi, name):
		server_db = sqlite3.connect(self.db_location);
		cursor = server_db.cursor();
		cursor.execute("Select * from ZONE_USERS where imsi=?", imsi);
		db_output = cursor.fetchall()
		if len(db_output) == 0:
			return False;
		else:
			return True;

	def get_gateways(self):
		
		nodes_db = sqlite3.connect(expanduser("~")+"/nodes");
		cursor = nodes_db.cursor();
		cursor.execute("select * from gateways where 1");
		output = cursor.fetchall();
		nodes_db.close();

		gateways = [];
		for i in range(len(output)):
			gateways.append(output[i][0]);

		return gateways;


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
	app.run();



