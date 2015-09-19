import syslog
import time
from freeswitch import *
from libvbts import FreeSwitchMessenger

def chat(message, args):
       # syslog.syslog("AALU: Inside chat")
	args = args.split("|")
	current_time = time.time()
	text_body = args[2]
	syslog.syslog("AALU: " + "Call time and message: " + str(current_time) + " " + str(text_body))

def fsapi(session, stream, env, args):
	chat(None, args)
