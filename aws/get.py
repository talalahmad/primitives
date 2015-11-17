import requests
import logging
import multiprocessing
import syslog


class get(multiprocessing.Process):
	def __init__(self, s, p, d):
		multiprocessing.Process.__init__(self)
		self.server = s;
		self.port = p;
		self.data = d; #this is the dictionary that needs to be sent to server by get. 
		# loglvl=logging.DEBUG;
		# logging.basicConfig(format=('%(asctime)s %(module)s %(funcName)s '
  #                                   '%(lineno)d %(levelname)s %(message)s'),
  #                           filename='/var/log/marketplace.log',level=loglvl)

	def run(self):
		try:
			url = self.server;
			r = requests.get(url, params=self.data)
		except requests.ConnectionError as e:
			print e
			syslog.syslog("AALU: %s" %str(e))
        #logging.info('Get response object')