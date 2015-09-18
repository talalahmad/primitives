import pylibmc
import time
import get
import syslog
import uploader

# logging.basicConfig(format='%(asctime)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s', filename='/var/log/audio-server.log', level=logging.INFO)

def doNothing():
	time.sleep(0.5)
def main():
	mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
	while True:
		head = mc.get('queue_head')
		tail = mc.get('queue_tail')
		if mc.get('queue_head') < mc.get('queue_tail') or mc.get(str(head)) is not None:
			#there is something in the queue
			item = mc.get(str(head)) #this item needs to be uploaded
			item = str(item)
			item = item.split(',')
			data_to_be_sent = {};
			#for i in range(0,len(item)):
			#	syslog.syslog("AALU: item["+str(i)+"] = "+ item[i])

			data_to_be_sent['i'] = item[0]
			data_to_be_sent['t'] = item[1]
			data_to_be_sent['d'] = item[2] #+","+item[3]+","+item[4]+","+item[5]
 
                        # logging.info('Item 1 %s' % item[0])
                        # logging.info('Item 2 %s' % item[1])
                        # logging.info('Item 3 %s' % item[2])
			if item[1] == 'MKP':
				data_to_be_sent['d'] = item[2] +","+item[3]+","+item[4]+","+item[5]
				thread = get.get('http://ec2-54-93-162-141.eu-central-1.compute.amazonaws.com:8080/server','',data_to_be_sent);
			#	thread = get.get('http://0.0.0.0:8888/server','',data_to_be_sent);
				thread.start();
				thread.join();
			#add if else based on the application for which data is being uploaded. 
			if item[1] == 'IVR':
				data_to_be_sent['d'] = item[2]
			#	thread = uploader.file_uploader('http://128.122.140.120:8888/ivr_server', '', data_to_be_sent['d'])
				thread = uploader.file_uploader('http://ec2-54-93-162-141.eu-central-1.compute.amazonaws.com:8080/server', '', data_to_be_sent['d'])
				thread.start()
				thread.join()
			
			if head < tail:
				mc.incr('queue_head')
			#else there is no need to increase the head location
			mc.delete(str(head))
		else:
			#the queue seems to be empty so do nothing. 
			#wait for a half a second and then ho out to the while again
			doNothing();


if __name__ == "__main__":
    main()
