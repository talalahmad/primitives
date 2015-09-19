import web
import requests
import pylibmc
import threading
import logging
import base

logging.basicConfig(format='%(asctime)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s', filename='/var/log/audio-server.log', level=logging.INFO)


def main():
    logging.info('In Init') 
    # url = 'http://10.0.0.1:8080/marketplace'
    mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
    logging.info('Mem Cache : %s' % str(mc))
    while True:
        with open('/home/cted-server/Primitives/primitives/ivr_audio_files.txt', 'r+') as ivr_audio_files:
            content = ivr_audio_files.readlines()
            #  logging.info('Content : %s' % content)
            if len(content) > 0:
	        # ivr_audio_files.seek(0)
		for content_item in content:
                    if content_item != '':
		        logging.info('Content Item : %s' % str(content_item))	
	                if mc.get('id') is None:
		            mc.set('id',0)
	                req_id = str(mc.get('id'))
	                mc['id'] = mc['id']+1
                        logging.info('Req Id : %s' % req_id)
                        base.POST(req_id, "IVR", str(content_item))
                       # params = {'i': req_id, 't': 'IVR', 'd': str(content_item)}
		       # r = requests.post(url, params=params)
		    # ivr_audio_files.write(content_item)
	        file = open('/home/cted-server/Primitives/primitives/ivr_audio_files.txt', 'w+')
	        file.close()
            else:
                ivr_audio_files.close()

		



if __name__ == "__main__":
	main()

                    




        
