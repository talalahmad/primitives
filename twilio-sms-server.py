#!/usr/bin/python
import threading
import traceback

import web
import requests

import syslog
import time
import random

import vbts_interconnects
from vbts_interconnects import vbts_twilio, vbts_voipms, vbts_util, vbts_fs, vbts_nexmo

from libvbts import Messenger

import vbts_credit

urls = ("/twilio_sms", "twilio_sms",
        "/nexmo_sms", "nexmo_sms",
        "/nexmo_file", "nexmo_file",
        "/nexmo_search", "nexmo_random_search",
        "/nexmo_get", "nexmo_random_get",
        "/nexmo_delivery", "nexmo_delivery",
        "/out_twilio_sms", "out_twilio_sms",
        "/out_nexmo_sms", "out_nexmo_sms",
        "/twilio_registration", "twilio_registration",
        "/voipms_registration", "voipms_registration",
        "/nexmo_registration", "nexmo_registration")

class registration:
    """
    Class for doing registration. POST request fires off a registration worker,
    which does allocates a new number, registers the phone, then sends the
    phone an SMS with the number.
    """
    def __init__(self):
        self.ic = None
        self.conf = vbts_util.get_conf_dict()
        self.worker = self.registration_worker
        self.fs_ic = vbts_fs.freeswitch_ic(self.conf)

    def registration_worker(self, from_name, ip, port, ret_num):
        try:
            number = self.ic.get_next_avail_number()
            if number:
                # register the user
                vbts_util.messenger.SR_provision(from_name, number, ip, port)
                self.fs_ic._send_raw_to_freeswitch(number, ret_num, "Your number is %s" % number)
                vbts_credit.log_credit(from_name, 0, 0, "Provisioned user %s number %s" % (from_name, number))
            else:
                # send failed message
                # TODO: how to send an SMS with no number provisioned??
                syslog.syslog("VBTS Failed to provision user %s" % from_name)
        except Exception as e:
            syslog.syslog("VBTS " + traceback.format_exc(e))

    def POST(self):
        data = web.input()
        needed_fields = ["from_name", "ip", "port", "ret_num"]
        if all(i in data for i in needed_fields):
            from_name = str(data.from_name)
            ip =  str(data.ip)
            port = str(data.port)
            ret_num = str(data.ret_num)
            t = threading.Thread(target=self.worker, kwargs={"from_name": from_name, "ip": ip, "port": port, "ret_num": ret_num})
            t.start()
            raise web.Accepted()
        else:
            raise web.NotFound()

class twilio_registration(registration):

    def __init__(self):
        registration.__init__(self)
        self.ic = vbts_twilio.twilio_ic(self.conf)

class voipms_registration(registration):

    def __init__(self):
        registration.__init__(self)
        self.ic = vbts_voipms.voipms_ic(self.conf)

class nexmo_registration(registration):

    def __init__(self):
        registration.__init__(self)
        self.ic = vbts_nexmo.nexmo_ic(self.conf)

class incoming_sms:

    def __init__(self):
        self.conf = vbts_util.get_conf_dict()
        self.fs_ic = vbts_fs.freeswitch_ic(self.conf)
        self.tariff_type = "incoming_sms"

    def bill(self, to, from_):
        syslog.syslog("VBTS " + to + " " + from_)
        try:
            tariff = vbts_credit.sms_cost(self.tariff_type)
            username = vbts_util.messenger.SR_dialdata_get("dial", ("exten", to))
            if (username and username != ""):
                vbts_credit.deduct(tariff, username, "Incoming SMS from %s to %s at %s" % (from_, to, self.tariff_type))
        except Exception as e:
            syslog.syslog("VBTS " + traceback.format_exc(e))


class twilio_sms(incoming_sms):
    """
    Class for handling incoming messages from Twilio.
    """
    def __init__(self):
        incoming_sms.__init__(self)

    def POST(self):
        data = web.input()
        needed_fields = ["Body", "To", "From", "ToCountry", "FromCountry"]
        if all(i in data for i in needed_fields):
            to = str(data.To)
            toCountry =  str(data.ToCountry)
            from_ = str(data.From)
            fromCountry = str(data.FromCountry)
            body = str(data.Body)
            self.fs_ic.send(to, from_, body, to_country=toCountry, from_country=fromCountry)
            self.bill(to, from_)
            web.header('Content-Type', 'text/xml')
            return '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
        else:
            raise web.NotFound()

class nexmo_file:
    def __init__(self):
        pass
    def GET(self):
        print "some shit"
#        syslog.syslog("RAPID: in GET of nexmo_file")
        user_data = web.input()
        if len(user_data) is 2:
            post_ret = user_data['ret']
            app = user_data['app']
            syslog.syslog("RAPID: post random ret:%s,%s,%s" %(post_ret,app,str(time.time())))

class nexmo_search:
    def __init__(self):
        pass

    def GET(self):
        data = web.input()
        filenames = data['result']
        search_id = data['id']
        openvpn_ip = '10.8.0.10'
        if filenames != '':
            filenames_list = filenames.split(',')
            random_filename = random.sample(filenames_list, 1)
            syslog.syslog("RAPID: Random search id %s and filename %s " %(search_id, random_filename));
            get_data = {'do': 'get', 'key': random_filename, 'ip': openvpn_ip}
            thread = get("http://10.0.0.1:8080/search_and_get_random", get_data)
            thread.start()

class nexmo_get:
    def __init__(self):
        pass

    def GET(self):
        data = web.input(myfile={})
        filedir = '/home/openbts/GetFiles'
        if 'myfile' in data: 
            filepath=data.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            syslog.syslog("RAPID: GET filename = %s" %filename)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            #syslog.syslog("AALU: in if")
            fout.write(data.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
            
class get(threading.Thread):
    def __init__(self, s, d):
        threading.Thread.__init__(self)
        self.server = s;       
        self.data = d; #this is the dictionary that needs to be sent to server by get. 
       
    def run(self):
        url = self.server;
        syslog.syslog("RAPID: Sending GET to "+str(url));
        r = requests.get(url, params=self.data)
        print "RAPID: Get response object"+str(r)



class nexmo_sms(incoming_sms):
    """
    Class for handling incoming messages from Nexmo.
    """
    def __init__(self):
        incoming_sms.__init__(self)

    def GET(self):
        data = web.input()
        needed_fields = ["text", "to", "msisdn"]
        if all(i in data for i in needed_fields):
            to = str(data.to)
            from_ = str(data.msisdn)
            body = str(data.text)
            current_time = time.time()
            syslog.syslog("RAPID: post sms ret:%s,%s,%s" %(body,app,str(time.time())));
            self.fs_ic.send(to, from_, body)
            # syslog.syslog("AALU: Response time and message: " + current_time + " " +  body)
            self.bill(to, from_)
            return web.ok
        else:
            return web.badrequest

class nexmo_delivery(incoming_sms):
    """
    Class for handling delivery receipts from Nexmo.
    """
    def __init__(self):
        incoming_sms.__init__(self)
        self.m = Messenger.Messenger()

    def GET(self):
        try:
            self.GET_fake()
        except Exception as e:
            syslog.syslog("VBTS " + traceback.format_exc(e))

    def GET_fake(self):
        data = web.input()
        needed_fields = ["status", "to", "msisdn"]
        if all(i in data for i in needed_fields):
            to = str(data.to)
            from_ = str(data.msisdn)
            status = str(data.status)
            if (self.m.SR_get("delivery_receipt", ("callerid", to)) != "yes"):
                pass
            elif (status == "delivered"):
                self.fs_ic.send(to, "101", "Message has been received by %s" % from_)
            elif (status == "accepted"):
                self.fs_ic.send(to, "101", "Message has been received by the service provider for %s" % from_)
            return web.ok
        else:
            return web.badrequest


class out_sms:

    """
    Class for handling outgoing messages, needed due to poor chatplan
    performance. We accept a request, return 202 Accepted immediately, then
    fire off a thread that does the actual request and issues the
    billing request if appropriate.
    """

    def __init__(self):
        self.conf = vbts_util.get_conf_dict()
        self.worker = self.sms_worker

    def POST(self):
        data = web.input()
        needed_fields = ["to", "from_number", "from_name", "body", "service_type"]
        if all(i in data for i in needed_fields):
            to = str(data.to)
            from_number = str(data.from_number)
            from_name = str(data.from_name)
            body = str(data.body)
            service_type = str(data.service_type)
            t = threading.Thread(target=self.worker, kwargs={"to": to, "from_num": from_number, "from_name": from_name, "body": body, "service_type": service_type})
            t.start()
            raise web.Accepted()
        else:
            raise web.NotFound()

    #default SMS worker thread
    def sms_worker(self, to, from_num, from_name, body, service_type):
        try:
            if self.ic.send(to, from_num, body):
                billing_url = self.conf['billing_url']
                requests.post(billing_url, data={"from_name": from_name, "destination": to, "service_type": service_type})
        except Exception as e:
            syslog.syslog("VBTS " + traceback.format_exc(e))


class out_twilio_sms(out_sms):

    def __init__(self):
        out_sms.__init__(self)
        self.ic = vbts_twilio.twilio_ic(self.conf)

class out_nexmo_sms(out_sms):

    def __init__(self):
        out_sms.__init__(self)
        self.ic = vbts_nexmo.nexmo_ic(self.conf)

app = web.application(urls, locals())

if __name__ == "__main__":
    app.run()
