import requests
import logging
import datetime
import time
import uploader


def main():

    now = datetime.datetime.now()

    while True:
        new_time = datetime.datetime.now()
        time_elapsed = new_time - now
        if time_elapsed.seconds > 5:
            now = new_time
            filename = str(now) + ".txt"
            random_text = ("Random text is going into this goddamn file and its so deep" + "\n") * 2000
            file_path = '/home/openbts/UploadFolder/' + filename.replace(" ", "")
            with open(file_path, "w+") as file_to_send:
                file_to_send.write(random_text)
                file_to_send.close()
                thread = uploader.file_uploader('http://10.0.0.1:9090/upload', '', file_path)
                thread.start()
                thread.join()



if __name__ == "__main__":
    main()
