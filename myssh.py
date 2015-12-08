import paramiko
#from scp import SCPClient

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

# def download_files(ip, key, filename):
# 	k = paramiko.RSAKey.from_private_key_file("/home/talal/Dropbox/aws/"+key)
# 	c = paramiko.SSHClient()
# 	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 	print "connecting"
# 	c.connect( hostname = ip, username = "ec2-user", pkey = k )
# 	print "connected"
# 	scp = SCPClient(c.get_transport());
# 	scp.get('/home/ec2-user/'+filename,'/home/talal/'+key.split(',')[0])
