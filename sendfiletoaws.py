import requests
import web
import syslog
import uploader

urls = (
      "/upload", "upload"
    )

class upload:
	def __init_(self):
		pass

	def POST(self):
	    syslog.syslog("AALU: In Upload POST")
            data = web.input(myfile={})
            syslog.syslog("AALU: Data " + str(data))
            filedir = '/home/cted-server/FilesToBeUploadedAWS' # change this to the directory you want to store the file in.
            if 'myfile' in data: # to check if the file-object is created
                filepath=data.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
                fout.write(data.myfile.file.read()) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.
                thread = uploader.file_uploader('http://ec2-54-93-162-141.eu-central-1.compute.amazonaws.com:8080/server', '', filedir + '/' + filename)
                thread.start()

app = web.application(urls, locals())
if __name__ == "__main__":
    syslog.syslog("AALU: Starting Upload web application")
    app.run()