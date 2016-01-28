import re
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import time as ti

def parse2(files):
	count = 0
	#channels[key] = [[time,value],[time,value]]
	channels = {}
	for f in files:
		for line in open(f,'r'):
			if "MeasurementReport" in line:
				count = count+1
				temp = line.split("MeasurementReport: ")[1]
				time = temp.split(" {")[0]
				#print time

				#COPY paste from below, need to change this. 
				answer = re.findall('{[0-9]*:.*[0-9]',line)
				# print answer[0]
				ans = answer[0][1:]
				ans = ans.split(', ')
				# print ans
				for item in ans:
					broken = item.split(': ')
					key = broken[0]
					value = broken[1]
					#print "%s,%s" %(key,value)
					if key not in channels:
						channels[key] = [];
					channels[key].append([time,value])


	print "*************"
	count_possitive = 0
	count_negative = 0
	last_count = 0;
	last_time = '';
	last = ''
	#channels_smaller = [time,value,number of times]
	channels_smaller = {}
	for channel in sorted(map(int,channels.keys())):
		for arraymember in channels[str(channel)]:
			#print arraymember
			if arraymember[1] != "-0.001":   #this is just counting the possitive 
				#print "%s,%s" %(channel,arraymember[0])
				count_possitive=count_possitive+1
			else:  #this is just counting the negative 
				count_negative = count_negative+1

			#this part makes the channels_smaller dictionary	channels_smaller = [start_time,value,number of times]
			if last == '':  #this handles the first ever arraymameber in the channels array
				last_time = arraymember[0]
				last = arraymember[1]
				last_count = 1
			elif arraymember[1] == last:  # this handles when the entry is the same as last 
				last_count = last_count+1
			elif arraymember[1] != last:   # this parts handles the changes in the channel
				if channel not in channels_smaller:
					channels_smaller[channel] = []
				channels_smaller[channel].append([last_time,last,last_count])
				last = arraymember[1]
				last_count = 1
				last_time = arraymember[0]
		if channel not in channels_smaller:
			channels_smaller[channel] = []
		channels_smaller[channel].append([last_time,last,last_count]) #This handles the last few in the loop when there is no change
		last_count = 0;
		last_time = '';
		last = ''

		#print "%s,%d,%d,%d" %(channel,count_possitive,count_negative, len(channels_smaller[channel]))
		count_possitive=0
		count_negative=0

	
	for channel in sorted(map(int,channels.keys())):
		if channel in [1,16,22,45,48,52,59,89,95]:
			yaxis2 = []
			xaxis2 = []
			yaxis3 = []
			xaxis3 = []
			current_second = 0
			time_based_array = {} #time based array for each channel to complement the aa graphs
			for arraymember in channels[str(channel)]:
				tm = ti.strptime(arraymember[0].split('.')[0],"%Y-%m-%d %H:%M:%S")
				time_in_seconds = (tm[1]*30*24*3600)+(tm[2]*24*3600)+(tm[3]*3600)+(tm[4]*60)+tm[5]
				#print seconds
				if current_second == 0:
					current_second = time_in_seconds;
				if time_in_seconds != current_second:
					current_second = time_in_seconds
				if current_second not in time_based_array:
					time_based_array[current_second] = 0		
				time_based_array[current_second] = time_based_array[current_second]+1

			current_second = 0

			current_minute = 0
			for key in sorted(time_based_array.keys()):
				if len(xaxis2) > 0 and xaxis2[-1]+1 != key-min(time_based_array.keys()):
					for i in range(xaxis2[-1]+1,key-min(time_based_array.keys())):
						xaxis3.append(i)
						yaxis3.append(0)

				xaxis2.append(key-min(time_based_array.keys()))
				yaxis2.append(time_based_array[key])

			yaxis3 = []
			xaxis3 = []
			for current_minute in range(0,1000):
				agg = 0
				if (current_minute*300)+min(time_based_array.keys()) > max(time_based_array.keys()):
					break;
				for i in range(current_minute*300,(current_minute+1)*300):
					if i+min(time_based_array.keys()) in time_based_array:
						agg = time_based_array[i+min(time_based_array.keys())]+agg
				xaxis3.append(current_minute*5)
				yaxis3.append(agg)



			plt.figure()
			#plt.plot(xaxis2,yaxis2,'b.',label="Measurement Report Count")
			plt.plot(xaxis3,yaxis3,'b-',label="Measurement Report Count Every 5 Minutes")
			plt.xlabel("Time in minutes")
			plt.ylabel("Number of measurement reports")
			plt.legend(loc=0);
			plt.savefig("ab"+str(channel))

	number_bw_detection = []
	last = ''
	last_number = 0
	for channel in channels_smaller:
		if len(channels_smaller[channel]) > 1:
			plt.figure()
			value_yaxis = []
			value_xaxis = []
			count = 0
			print "********"
			for arraymember in channels_smaller[channel]:
				#print arraymember
				for i in range(0,arraymember[2]):
					if arraymember[1] < 0:
						arraymember[1] = 0
						print arraymember[1]
					value_yaxis.append(float(arraymember[1]))
					#print arraymember
					value_xaxis.append(count)
					count = count+1

				#channels_smaller = {[start_time,value,number of times]}
			for arraymember in channels_smaller[channel]:
				if last == '':
					last = arraymember[1]
					last_number = arraymember[2]
				if arraymember[1] != last and (last < 0 or last[0]=='-'):
					number_bw_detection.append(last_number)
				last = arraymember[1]
				last_number = arraymember[2]
			print "channel = %d and number_bw_detection length = %d"  %(channel,len(number_bw_detection))
			if len(number_bw_detection) > 0:
				print "min = %d and max = %d and avg = %f" %(min(number_bw_detection),max(number_bw_detection),sum(number_bw_detection)/len(number_bw_detection)) 
			number_bw_detection = []
			last = ''
			last_number = 0

			plt.plot(value_xaxis,value_yaxis,'b.', label="RSSI values reported")#,legand="Values Reported in Measurement Report")
			plt.ylabel("RSSI value")
			plt.xlabel("Cronologically arraged Measurement Reports")
			plt.legend(loc=0)
			plt.savefig("aa"+str(channel))
	print channels_smaller[48]


def parse(f, readings):
	for line in open(f,'r'):
		# print line
		answer = re.findall('{[0-9]*:.*[0-9]',line)
		# print answer[0]
		ans = answer[0][1:]
		ans = ans.split(', ')
		# print ans
		for item in ans:
			broken = item.split(': ')
			key = broken[0]
			value = broken[1]
			# print "key = %s and value = %s" %(key,value)
			if key in readings:
				readings[key].append(value)
			else:
				readings[key] = []
				readings[key].append(value)
	return readings;

def makefigure(files, savename):
	readings = {}
	for f in files:
		readings = parse(f, readings);
	# readings = parse("/home/alfred/24-09-15/pico_cell/New_Whitespace/report2.log", readings);
	# readings = parse("/media/UUI/whitespace_third/measurement_report_final_set", readings);
	# print result


	print "***************"

	channel_energy_dict = {}

	for key in sorted(readings):
		sum = 0.0
		for entry in readings[key]:
			if entry[0] is '-':
				sum = sum + 0
			else:
				sum = sum + float(entry)        
		# print "key = %s and number of readings = %d and sum = %f" %(key, len(readings[key]), sum)
		channel_energy_dict[key]=(sum)

	for i in range(0,120):
		if str(i) not in channel_energy_dict:
			print i
	#print "Channel Energy Dictionary %s" % str(channel_energy_dict)
	print len(channel_energy_dict)
	channels = []
	#frequency = [0.2] * 118
	frequency = [0.2]*len(channel_energy_dict)
	colors = []
	labels = []
	width = 1.0

	print "Length of frequency list %d" % len(frequency)

	for channel in channel_energy_dict.keys():
		channel_edited = channel.replace("'", "")
		#print channel_edited
		#print channel_energy_dict[channel]
		channels.append(float(channel))
		#print "Channels %s" % channels
		if channel_energy_dict[channel_edited] != 0:
			colors.append('r')
		    # labels.append('Unused Channels')
		else:
			colors.append('g')
	    	# labels.append('Used Channels')

	print "Length of Channel list %d" % len(channels)


	#print "Frequency %s" % frequency
	red_patch = mpatches.Patch(color='r')
	green_patch = mpatches.Patch(color='g')
	plt.figure()
	plt.bar(channels, frequency, width=width, color=colors, edgecolor='none')
	plt.xlabel('Channels')
	plt.ylabel('Frequency(MHz)')
	plt.title('Whitespaces Measurement')

	plt.legend((red_patch, green_patch), ('Used Channels', 'Unused Channels'))
	plt.savefig(savename)

files_2nd_week = ["/home/alfred/24-09-15/pico_cell/New_Whitespace/report1.log","/home/alfred/24-09-15/pico_cell/New_Whitespace/report2.log"]
makefigure(files_2nd_week, 'Whitespaces_2nd_week')

files_1st_week = ["/home/alfred/WHITESPACES/measurement_report_first_set","/home/alfred/WHITESPACES/measurement_report_second_set","/home/alfred/WHITESPACES/measurement_report_final_set"]
makefigure(files_1st_week, 'Whitespaces_1st_week')

#parse2(["/home/alfred/24-09-15/pico_cell/New_Whitespace/report1.log","/home/alfred/24-09-15/pico_cell/New_Whitespace/report2.log"])
#parse2(["/home/talal/Dropbox/primitives/New Whitespaces/report1.log","/home/talal/Dropbox/primitives/New Whitespaces/report2.log"])
parse2(files_1st_week)