import requests

class file_uploader(threading.Thread):
	def __init__(self,s,p,f):
		self.server = s;
		self.port = p;
		self.file_to_upload = f;


	def run(self):
		url = 'http://'+self.server+':'+self.port+'/'+postHandler
		files = {'file': open('"/home/talal/uploads/'+self.file_to_upload+'"','rb')}
		r = request.post(url, files=files)
		logging.info('Upload File Name: '+self.file_to_upload+' Status:'+ str(r.status_code))
		 

	
