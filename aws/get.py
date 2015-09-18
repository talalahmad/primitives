import requests
import logging
import threading

class get(threading.Thread):
	def __init__(self, s, p, d):
		threading.Thread.__init__(self)
		self.server = s;
		self.port = p;
		self.data = d; #this is the dictionary that needs to be sent to server by get. 
		# loglvl=logging.DEBUG;
		# logging.basicConfig(format=('%(asctime)s %(module)s %(funcName)s '
  #                                   '%(lineno)d %(levelname)s %(message)s'),
  #                           filename='/var/log/marketplace.log',level=loglvl)

	def run(self):
		url = self.server;
		r = requests.get(url, params=self.data)
        logging.info('Get response object')