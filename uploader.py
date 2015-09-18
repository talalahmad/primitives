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
		files = {'myfile': open(self.file_to_upload.replace("\n", ""),'rb')}
		r = requests.post(url, files=files);
		syslog.syslog('AALU: Upload File Name: '+self.file_to_upload+' Status:'+str(r.status_code));
		 

	
