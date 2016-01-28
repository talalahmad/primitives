
import matplotlib.pyplot as plt 
import numpy as np 
## agg backend is used to create plot as a .png file
#mpl.use('agg')

import matplotlib.pyplot as plt 

def stats(d5, start_time_500, d_initial5={}):
	dif_500_dht = [];
	for key in d5:
		if key in d_initial5:
			dif_500_dht.append(float(d5[key][0])-float(d_initial5[key][0]))
	dif_500_dht = np.array(dif_500_dht)
	m = np.mean(dif_500_dht)
	std = np.std(dif_500_dht)
	sorted_data = np.sort(dif_500_dht)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	print "xxxx"
	print "%f,%f" %(m,std)
	print "xxxx"
	return (sorted_data,yvals)

def stats2(d5, start_time_500, d_initial5={}):
	dif_500_dht = [];
	for key in d5:
		dif_500_dht.append(float(d5[key][0])-float(start_time_500))
	dif_500_dht = np.array(dif_500_dht)
	m = np.mean(dif_500_dht)
	std = np.std(dif_500_dht)
	sorted_data = np.sort(dif_500_dht)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	print "xxxx"
	print "%f,%f" %(m,std)
	print "xxxx"
	return (sorted_data,yvals)

def parse_cl_again(current_file):
	timesaved_count = 0;
	times = dict();
	times_temp = {}
	times_start_temp = {}
	start_time = 0;
	#current_file = 500; #DO: make this argument? 
	
	filename = "frankfurt/log_cl_again_"+str(current_file);
	#print filename;
	op = open(filename,'r')
	for line in op:
		if "BALU" in line:
			if "BALU: Starting web application" in line: # find the last "Starting web application"
				times = {}
				times_start_temp = {}
				timesaved_count = 0;

			if "BALU: uid=100000000000 and time=" in line and "frankfurt" in filename:
				start_time = line.split("BALU: uid=100000000000 and time=")[1][:-1]
				#print "starting time = %s" %start_time

			if "time=" in line and "uid=" in line: #TO record initialization times
					#print line
					l = line.split("BALU: uid=")
					key = l[1].split()[0]
					if key not in times_start_temp:
					#	print "something added"
						times_start_temp[key] = []
						times_start_temp[key].append(line.split("time=")[1][:-1])

			if "uid" in line and "timesaved" in line:
				#print "here"
				l = line.split("BALU: uid=")
				key = l[1].split()[0]
				
				if key not in times:
					times[key] = []
					times[key].append(line.split("timesaved=")[1][:-1])
				else:
					times[key] = []
					temp = line.split("timesaved=")[1][:-1];
					times[key].append(temp)
	op.close();
	#print op.closed

	ret = dict();				
	for i in range(0,current_file-(current_file/10)):
		uid = 100000000000+i
		if str(uid) in times:
			#print "uid=%s and timesaved=%s" %(str(uid),times[str(uid)])
			ret[str(uid)]=times[str(uid)]
	return [ret,start_time, times_start_temp]

def parse_dht(current_file):
	timesaved_count = 0;
	times = dict();
	times_temp = {}
	times_start_temp = {}
	start_time = 0;
	#current_file = 500; #DO: make this argument? 
	locations = ["frankfurt","california","ireland","singapore","tokyo","oregon","saopaulo","sydney","virginia"]
	for loc in locations:
		#print loc
		filename = loc+"/log_dht_"+str(current_file);
		#print filename;
		op = open(filename,'r')
		for line in op:
			if "BALU" in line:
				if "BALU: Starting web application" in line or "starter starting here here here" in line: # find the last "Starting web application"
					times_temp[loc] = {}

				if ("BALU: Starting web application" in line or "starter starting here here here" in line) and loc == "frankfurt": # find the last "Starting web application"
					times_start_temp = {}
					#print "something cleaned"

				if "BALU: uid=100000000000 and time=" in line and "frankfurt" in filename:
					start_time = line.split("BALU: uid=100000000000 and time=")[1][:-1]
					#print "starting time = %s" %start_time

				if loc is "frankfurt" and "time=" in line and "uid=" in line: #TO record initialization times
					#print line
					l = line.split("BALU: uid=")
					key = l[1].split()[0]
					if key not in times_start_temp:
					#	print "something added"
						times_start_temp[key] = []
						times_start_temp[key].append(line.split("time=")[1][:-1])

				if "uid" in line and "timesaved" in line:
					#print "here"
					l = line.split("BALU: uid=")
					key = l[1].split()[0]
					
					if key not in times_temp[loc]:
						times_temp[loc][key] = []
						times_temp[loc][key].append(line.split("timesaved=")[1][:-1])
					# else:
					# 	times[key] = []
					# 	temp = line.split("timesaved=")[1][:-1];
					# 	times[key].append(temp)
		op.close();
		#print op.closed


	ret = dict();	
	for loc in locations:
		ret.update(times_temp[loc])			
	# for i in range(0,current_file):
	# 	uid = 100000000000+i
	# 	if str(uid) in times:
	# 		#print "uid=%s and timesaved=%s" %(str(uid),times[str(uid)])
	# 		ret[str(uid)]=times[str(uid)]
	return [ret,start_time,times_start_temp]




sorted_data = []
yvals = []

d5 = {}
d_initial5 = {};
start_time_500 = 0;
line1,line2 = [],[]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Time in seconds")
ax.set_ylabel("CDF")
data_to_be_plotted_dht = []
for i in range(0,5):
	[d5,start_time_500,d_initial5] =  parse_dht(500*(i+1));
	print len(d5)
	print len(d_initial5)
	#line1.append(stats(d5,start_time_500))
	[sorted_data,yvals] = stats(d5,start_time_500,d_initial5)
	data_to_be_plotted_dht.append(stats2(d5,start_time_500,d_initial5)[0])
	ax.plot(sorted_data, yvals, 'r-')


##CHANGE NAMES ACCORDINGLY (reusing from above for now. )
data_to_be_plotted_cl = []
for i in range(0,5):
	[d5,start_time_500,d_initial5] =  parse_cl_again(500*(i+1));
	print len(d5)
	print len(d_initial5)
	[sorted_data,yvals] = stats(d5,start_time_500,d_initial5)
	data_to_be_plotted_cl.append(stats2(d5,start_time_500,d_initial5)[0])
	ax.plot(sorted_data, yvals, 'b-')

a = [int((i+1)*500) for i in range(0,5)]
b = [float(i[0]) for i in line1]
berr = [float(i[1]) for i in line1]
c = [float(i[0]) for i in line2]
cerr = [float(i[1]) for i in line2]
plt.savefig("times_cdf");
fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(data_to_be_plotted_dht, 0, '')
fig.savefig('box_dht', bbox_inches='tight')

fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(data_to_be_plotted_cl)
fig.savefig('box_cl')

data_combined_alternate = []
for i in range(0,len(data_to_be_plotted_cl)):
	data_combined_alternate.append(data_to_be_plotted_cl[i])
	data_combined_alternate.append(data_to_be_plotted_dht[i])

fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(data_combined_alternate, notch=True, patch_artist=True)
ax.set_xticklabels(['450','450', '900','900', '1350','1350', '1800','1800','2250','2250'])
boxColors = ['darkkhaki', 'royalblue','darkkhaki', 'royalblue','darkkhaki', 'royalblue','darkkhaki', 'royalblue','darkkhaki', 'royalblue']
for patch, color in zip(bp['boxes'],boxColors):
	patch.set_facecolor(color)

plt.figtext(0.2, 0.8,'Client-Server Model',
            backgroundcolor=boxColors[0], color='black', weight='roman',
            size='x-small')
plt.figtext(0.2, 0.765, 'DHT Model',
            backgroundcolor=boxColors[1],
            color='white', weight='roman', size='x-small')
ax.set_ylabel('Time in seconds')
ax.set_xlabel('Number of Users')

fig.savefig('box_combined')

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xlabel("Number of users")
# ax.set_ylabel("Time in seconds")
# ax.axis([0,3000,0,50])

# ax.plot(a, b, 'r--')
# ax.errorbar(a,b,yerr=berr)
# ax.plot(a, c, 'b--')
# ax.errorbar(a,c,yerr=cerr)



# print "[%d,%d,%d,%f]" % (oe,cr,to,sum(ret_times)/float(len(ret_times)))
# a = np.array(ret_times)
# print min(ret_times)
# print np.percentile(a,25)
# print np.percentile(a,50)
# print np.percentile(a,75)
# print max(ret_times)
# data_to_plot.append(a);
# oe_counts.append(oe)
# cr_counts.append(cr)
# to_counts.append(to)

# [oe,cr,to,ret_times] = parse("200_distributed");
# print "[%d,%d,%d,%f]" % (oe,cr,to,sum(ret_times)/float(len(ret_times)))
# a = np.array(ret_times)
# data_to_plot.append(a);
# print min(ret_times)
# print np.percentile(a,25)
# print np.percentile(a,50)
# print np.percentile(a,75)
# print max(ret_times)
# oe_counts.append(oe)
# cr_counts.append(cr)
# to_counts.append(to)

# [oe,cr,to,ret_times] = parse("300_distributed");
# a = np.array(ret_times)
# data_to_plot.append(a);
# print "[%d,%d,%d,%f]" % (oe,cr,to,sum(ret_times)/float(len(ret_times)))
# print min(ret_times)
# print np.percentile(a,25)
# print np.percentile(a,50)
# print np.percentile(a,75)
# print max(ret_times)
# oe_counts.append(oe)
# cr_counts.append(cr)
# to_counts.append(to)

# [oe,cr,to,ret_times] = parse("400_distributed");
# a = np.array(ret_times)
# data_to_plot.append(a);
# print "[%d,%d,%d,%f]" % (oe,cr,to,sum(ret_times)/float(len(ret_times)))
# print min(ret_times)
# print np.percentile(a,25)
# print np.percentile(a,50)
# print np.percentile(a,75)
# print max(ret_times)
# oe_counts.append(oe)
# cr_counts.append(cr)
# to_counts.append(to)

# # [oe,cr,to,ret_times] = parse("500");
# # a = np.array(ret_times)
# # data_to_plot.append(a);
# # print "[%d,%d,%d,%f]" % (oe,cr,to,sum(ret_times)/float(len(ret_times)))
# # print min(ret_times)
# # print np.percentile(a,25)
# # print np.percentile(a,50)
# # print np.percentile(a,75)
# # print max(ret_times)
# # oe_counts.append(oe)
# # cr_counts.append(cr)
# # to_counts.append(to)

# # Create a figure instance
# #fig = plt.figure()
# # Create an axes instance
# fig = plt.figure(1, figsize=(9, 6))
# ax = fig.add_subplot(111)

# # Create the boxplot
# bp = ax.boxplot(data_to_plot)

# ax.set_xticklabels([100,200,300,400,500])
# plt.ylabel("Time in seconds")
# # Save the figure
# fig.savefig('fig1_distributed.png', bbox_inches='tight')

# plt.figure()
# plt.plot([100,200,300,400],oe_counts,'gx-',label='Operational Error')
# plt.plot([100,200,300,400],cr_counts,'rd-',label='Connection Reset')
# plt.plot([100,200,300,400],to_counts,'bo-',label='Time Out')
# plt.ylabel("Number of filures")
# plt.legend(loc=0)

# plt.savefig('fig2_distributed.png')



def parse(filename):
	times500 = dict();
	times1000 = dict();
	times1500 = dict();
	times2000 = dict();
	times2500 = dict();
	start500 = 0;
	start1000 = 0;
	start1500 = 0;
	start2000 = 0;
	start2500 = 0;


	times = dict();
	ret_times = []
	for line in open(filename,'r'):
		if "BALU" in line:
			if "starter starting here here here" in line:
				times = {}

			if "Number of users=500 Ending" in line:
				times500 = times;
				times = {};
			elif "Number of users=1000 Ending" in line:
				times1000 = times;
				times={}
			elif "Number of users=1500 Ending" in line:
				times1500 = times;
				times={}
			elif "Number of users=2000 Ending" in line:
				times2000 = times;
				times={}
			elif "Number of users=2500 Ending" in line:
				times2500 = times;
				times={} 
			
			if "uid" in line:
				l = line.split("BALU: uid=")
				key = l[1].split()[0]
				#print key
				if key not in times:
					times[key] = []
					times[key].append(line.split("time=")[1][:-1])
				else:
					times[key].append(line.split("time=")[1][:-1])

			if "Number of users=500 Starting" in line:
				start_500 = line.split("Number of users=500 Starting time=")[1][:-1]
			elif "Number of users=1000 Starting" in line:
				start_1000 = line.split("Number of users=1000 Starting time=")[1][:-1]
			elif "Number of users=1500 Starting" in line:
				start_1500 = line.split("Number of users=1500 Starting time=")[1][:-1]
			elif "Number of users=2000 Starting" in line:
				start_2000 = line.split("Number of users=2000 Starting time=")[1][:-1]
			elif "Number of users=2500 Starting" in line:
				start_2500 = line.split("Number of users=2500 Starting time=")[1][:-1]


	return [times500,times1000, times1500, times2000, times2500, start_500, start_1000, start_1500, start_2000, start_2500]