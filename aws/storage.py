import sqlite3
from os.path import expanduser

class storage:
	def __init__(self):
		self.db_location = expanduser("~")+"/gateway.db";
		#self.name = name;
		#self.hash = hash.Hash(self.get_gateways);
		server_db = sqlite3.connect(self.db_location);
		cursor = server_db.cursor();
		cursor.execute("CREATE TABLE IF NOT EXISTS ZONE_USERS (TSTAMP TIMESTAMP, IMSI VARCHAR(16), NAME VARCHAR(16), BTS VARCHAR, RESOLVER VARCHAR);");
		cursor.execute("CREATE TABLE IF NOT EXISTS RESOLVED (TSTAMP TIMESTAMP, IMSI VARCHAR(16), NAME VARCHAR(16), BTS VARCHAR, GATEWAY VARCHAR);");
		server_db.commit();
		server_db.close();

	def GET(self, user_data):
	#	user_data= web.input();

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
