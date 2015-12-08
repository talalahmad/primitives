import paramiko

def(ip):
	k = paramiko.RSAKey.from_private_key_file("/home/talal/Dropbox/aws/frankfurt.pem")
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "connecting"
	c.connect( hostname = "52.29.148.194", username = "ec2-user", pkey = k )
	print "connected"
	commands = [ "ls" ]
	for command in commands:
		print "Executing {}".format( command )
		stdin , stdout, stderr = c.exec_command(command)
		print stdout.read()
		print( "Errors")
		print stderr.read()
	c.close()
