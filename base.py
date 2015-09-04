#using 3 digit codes to hightlight the type of applcation to assign priority later. 
#TODO: It should be a priority queue and not a normal queue. 
class primitives:
	
	def __init__(self, ip, port):
		#server_type variable indicates if using hash.py or central.py
		self.server_type=central;
		self.server_ip = ip;
		self.server_ip = port;
		self.queue=[]
		self.uploader = '';

#i is identity, t is type of application, d is data/file name
	def POST(self,i,t,d):
		#Put this in the queue to be uploaded to server based on server type
		item = {};
		item['ID'] = identity;
		item['Type'] = t;
		item['File'] = d;

		self.queue.append(item)



	def GET(self,identity):
		#Get data with this identity from the server


	def SEARCH(self,type,data):
		#Search data at the server

	def SEND(self,type,data,to):
		#send data from the server to the respective user in a lazy manner. Don't know about this for now.  

	def main(self, server_ip, server_port):
		while True:
			if len(queue) > 0:
				item = queue.pop();
				if !self.uploader.is_alive():
					if item['Type'] is 'IVR':
						self.uploader = file_uplaoder(self.server_ip,self.server_port,item['File']);
						self.uploader.start();

					if item['Type'] is 'MPL':
						self.uploader = file_uplaoder(self.server_ip,self.server_port,item['File']);
						self.uploader.start();
				else:
					logging.info("waiting for thread to complete");

