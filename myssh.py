import paramiko

def connect_after(ip, key, how_many):
	k = paramiko.RSAKey.from_private_key_file("/home/ec2-user/"+key)
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "connecting"
	c.connect( hostname = ip, username = "ec2-user", pkey = k )
	print "connected"
	commands = ["cat /proc/net/dev > ~/bandwidth_after_dht_"+str(how_many) ,"sudo grep BALU /var/log/messages > ~/log_dht_"+str(how_many)]
	for command in commands:
		print "Executing {}".format( command )
		stdin , stdout, stderr = c.exec_command(command)
		print stdout.read()
		print( "Errors")
		print stderr.read()
	c.close()

def connect_before(ip, key, how_many):
	k = paramiko.RSAKey.from_private_key_file("/home/ec2-user/"+key)
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "connecting"
	c.connect( hostname = ip, username = "ec2-user", pkey = k )
	print "connected"
	commands = ["python ~/primitives/aws/node.py 8080 &" ,"cat /proc/net/dev > ~/bandwidth_before_dht_"+str(how_many)]
	for command in commands:
		print "Executing {}".format( command )
		stdin , stdout, stderr = c.exec_command(command)
		print stdout.read()
		print( "Errors")
		print stderr.read()
	c.close()
