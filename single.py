import requests
import logging
import datetime
import time
import uploader
import syslog
#RUN this code should run in the BTS node. 
def main():
    new_time = datetime.datetime.now()
    now = new_time
    #RUN: change the ip to mention the source
    filename = "SEN:10.8.0.6:"+str(now) + ".txt"
    random_text = ("Random text is going into this goddamn file and its so deep" + "\n") * 2000
    #RUN: foldername needs to be changed based on the machine usage. 
    file_path = '/home/talal/UploadFolder/' + filename.replace(" ", "")
    with open(file_path, "w+") as file_to_send:
        file_to_send.write(random_text)
        file_to_send.close()
        syslog.syslog("RAPID: Random file:%s at time:%s" %(filename.replace(" ",""),str(time.time())))
        #RUN: change the ip and port below based on what is your local server 
        thread = uploader.file_uploader('http://10.8.0.1:8080/upload', '', file_path)
        thread.start()
        thread.join()



if __name__ == "__main__":
    main()
