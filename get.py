import requests

class get(threading.Thread):
	def __init__():
		self.server = '';
		self.port = '';
		self.data = {}; #this is the dictionary that needs to be sent to server by get. 


	def run():
		url = 'http://'+self.server+':'+self.port+'/'+postHandler
        r = requests.get(url, params=data)
		logging.info('Upload File Name: '+self.file_to_upload+' Status:'+ str(r.status_code))