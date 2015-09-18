import pylibmc
import syslog

#using 3 digit codes to hightlight the type of applcation to assign priority later. 
#TODO: It should be a priority queue and not a normal queue. 
#class primitives:


# TODO: basically have to impliment a queue in pylibmc. 
#i is identity, t is type of application, d is data/file name
def POST(i,t,d):
	#Put this in the queue to be uploaded to server based on server type
	mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
	if mc.get('queue_head') is None:
		mc['queue_head'] = -1; #this contains the head of the queue that exists in mc, value of -1 means that the queue is empty. 
	if mc.get('queue_tail') is None:
		mc['queue_tail'] = -1; # this contains the tail of the queue that exists in mc, value of -1 means that the queue is empty.
	#syslog.syslog("AALU: i="+i+",t="+t+",d="+d)
	if mc.get('queue_tail') == mc.get('queue_head') and mc.get(str(mc.get('queue_head'))) is not None:
	 	mc.incr('queue_tail')
		mc.set(str(mc.get('queue_tail')),i+","+t+","+d)
		#mc.incr('queue_head')
	elif mc.get('queue_tail') == mc.get('queue_head'):
		mc.set(str(mc.get('queue_tail')),i+","+t+","+d)
	else:
		mc.incr('queue_tail')
		mc.set(str(mc.get('queue_tail')),i+","+t+","+d)


#		self.queue.append(item)



	# def GET(self,identity):
	# 	#Get data with this identity from the server
	# def SEARCH(self,type,data):
	# 	#Search data at the server

	# def SEND(self,type,data,to):
	# 	#send data from the server to the respective user in a lazy manner. Don't know about this for now.  

	# def main(self, server_ip, server_port):
	# 	while True:
	# 		if len(queue) > 0:
	# 			item = queue.pop();
	# 			if !self.uploader.is_alive():
	# 				if item['Type'] is 'IVR':
	# 					self.uploader = file_uplaoder(self.server_ip,self.server_port,item['File']);
	# 					self.uploader.start();

	# 				if item['Type'] is 'MPL':
	# 					self.uploader = file_uplaoder(self.server_ip,self.server_port,item['File']);
	# 					self.uploader.start();
	# 			else:
	# 				logging.info("waiting for thread to complete");

