import re
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


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

def makefigure(files, savename)
	readings = {}
	for file in files:
		readings = parse("/home/alfred/24-09-15/pico_cell/New_Whitespace/report1.log", readings);
	readings = parse("/home/alfred/24-09-15/pico_cell/New_Whitespace/report2.log", readings);
	# readings = parse("/media/UUI/whitespace_third/measurement_report_final_set", readings);
	#print result
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
	frequency = [0.2]*106
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
	plt.savefig("whitespaces_image")

files_2nd_week = ["/home/alfred/24-09-15/pico_cell/New_Whitespace/report1.log","/home/alfred/24-09-15/pico_cell/New_Whitespace/report2.log"]
makefigure(files_2nd_week, 'Whitespaces_2nd_week')