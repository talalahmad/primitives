import requests
import syslog
import threading

class file_uploader(threading.Thread):
	def __init__(self,s,p,f):
		threading.Thread.__init__(self)
		self.server = s;
		self.port = p;
		self.file_to_upload = f;


	def run(self):
		url = self.server
		#RUN: see the below line and change the ip
		files = {'myfile': open(self.file_to_upload.replace("\n", ""),'rb'),'myself':'10.8.0.6'}
		data = {};
		r = requests.post(url, files=files);
		syslog.syslog('AALU: Upload File Name: '+self.file_to_upload+' Status:'+str(r.status_code));
		 

	
