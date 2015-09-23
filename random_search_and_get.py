import requests
import datetime
import time
import pylibmc

def main():
    now = datetime.datetime.now()
    openvpn_ip = '10.8.0.10'
    other_user_openvpn_ip = '10.8.0.6'
    mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

    while True:
        new_time = datetime.datetime.now()
        time_elapsed = new_time - now
        if time_elapsed.seconds > 60:
        	now = new_time
        	if mc.get('id') is None:
			    mc.set('id',0)
		    req_id = str(mc.get('id'))
		    mc['id'] = mc['id']+1
        	get_params = {'do': 'search', 'key': other_user_openvpn_ip, 'ip': openvpn_ip, 'id': req_id}
        	r = request.get("http://10.0.0.1:8080/search_and_get_random", params=get_params)


if __name__ = "__main__":
	main()


