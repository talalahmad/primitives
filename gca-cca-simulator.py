import numpy.random as random
import numpy as np
import matplotlib.pyplot as plt

#assuming packet gateways are in the cloud 
#no data/sms based communication can happen if the
def call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,ratio): 
	exact_failure = random.choice(num_of_layer1_nodes)
	#tc,ts and td contain the layers contribution of call,sms and data
	icall = np.around((calls_in_epoch*ratio)/num_of_layer1_nodes)
	isms = np.around((sms_in_epoch*ratio)/num_of_layer1_nodes)
	idata = np.around((data_in_epoch*ratio)/num_of_layer1_nodes)

	if icall >= 1:
		round_call_loss = icall
	elif calls_in_epoch * ratio < exact_failure:
		round_call_loss = 0
	else:
		round_call_loss = 1

	return [round_call_loss,round_call_loss*2,round_call_loss*1.5]

def simulate(num_of_layer1_nodes, min_calls, multiplier):
#	cloud_server = True;
#	num_of_layer1_nodes = 10;
#	num_of_layer2_nodes = 10;
#	users_l1_node = 500; 
#	users_l2_node = users_l1_node*0.8;
	cp_bw_l1_l2 = 40
	cp_at_l1 = 20
	cp_bw_l1_outside = 40
	time_cycles = 3600
	l1_over_l2_users = 1.5

	round_call_loss = 0;
	round_sms_loss = 0;
	round_data_loss = 0;

	round_cloud_pgw_loss = [0,0,0];

	call_loss = 0
	data_loss = 0
	sms_loss = 0

	cloud_pgw_loss = [0,0,0]

	successful_calls = 0
	successful_sms = 0
	successful_data = 0

	cloud_pgw_success = [0,0,0]

	for i in range(0,time_cycles):
		calls_in_epoch = random.random_integers(min_calls, num_of_layer1_nodes * multiplier)
		sms_in_epoch = random.random_integers(min_calls, calls_in_epoch*1.75 )
		data_in_epoch = random.random_integers(min_calls, (calls_in_epoch)*1.5 )
		#print "%d,%d" %(i,calls_in_epoch)
		node_failing = random.choice((num_of_layer1_nodes*4)+1)
		if node_failing == 0:
			round_call_loss = 0;
			round_sms_loss = 0;
			round_data_loss = 0
			round_cloud_pgw_loss = [0,0,0]

		elif node_failing <= (1 * num_of_layer1_nodes): #lowest layer failure
			[round_call_loss,round_sms_loss,round_data_loss] = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.4);
			round_cloud_pgw_loss = [round_call_loss,round_sms_loss,round_data_loss]

		elif node_failing <= (2 * num_of_layer1_nodes): # link between l1 and l2
			temp = []
			temp = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.4);
			[round_call_loss,round_sms_loss,round_data_loss] = np.around([temp[0]*0.8,temp[1]*0.8,temp[2]*0.8])
			round_cloud_pgw_loss = np.around([temp[0],temp[1],temp[2]])

		elif node_failing <= (3 * num_of_layer1_nodes): # node in l2 and cloud
			temp = []
			temp = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.4);
			[round_call_loss,round_sms_loss,round_data_loss] = np.around([temp[0]*0.8,temp[1]*0.8,temp[2]*0.8])
			temp2 = []
			temp2 = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.6);
			
			round_call_loss = round_call_loss+temp2[0]
			round_sms_loss = round_sms_loss+temp2[1]
			round_data_loss = round_data_loss+temp2[2]

			round_cloud_pgw_loss = [temp[0]+temp2[0],temp[1]+temp2[1],temp[2]+temp2[2]]
		
		elif node_failing <= (4 * num_of_layer1_nodes): # link between l2 and cloud
			temp = []
			temp = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.4);
			[round_call_loss,round_sms_loss,round_data_loss] = np.around([temp[0]*0.4,temp[1]*0.4,temp[2]*0.4])
			temp2 = []
			temp2 = call_sms_data_failure_at(calls_in_epoch,sms_in_epoch,data_in_epoch,num_of_layer1_nodes,0.6);
			[round_call_loss2,round_sms_loss2,round_data_loss2] = np.around([temp2[0]*0.8,temp2[1]*0.8,temp2[2]*0.8])

			round_call_loss = round_call_loss+round_call_loss2
			round_sms_loss = round_sms_loss+round_sms_loss2
			round_data_loss = round_data_loss+round_data_loss2

			round_cloud_pgw_loss = [temp[0]+temp2[0],temp[1]+temp2[1],temp[2]+temp2[2]]
			
		#print "%d,%d,%d" %(round_call_loss,round_sms_loss,round_data_loss)

		call_loss = call_loss + round_call_loss
		sms_loss = sms_loss + round_sms_loss
		data_loss = data_loss + round_data_loss

		successful_calls = successful_calls + (calls_in_epoch - round_call_loss);
		successful_sms = successful_sms + (sms_in_epoch - round_sms_loss)
		successful_data = successful_data + (data_in_epoch - round_data_loss)

		cloud_pgw_loss = [x + y for x, y in zip(cloud_pgw_loss, round_cloud_pgw_loss)]
		second = [calls_in_epoch - round_cloud_pgw_loss[0], sms_in_epoch - round_cloud_pgw_loss[1], data_in_epoch - round_cloud_pgw_loss[2]]
		cloud_pgw_success = [x + y for x, y in zip(cloud_pgw_success, second)]

	return [[call_loss,sms_loss,data_loss,successful_calls,successful_sms,successful_data],[cloud_pgw_loss[0],cloud_pgw_loss[1],cloud_pgw_loss[2],cloud_pgw_success[0],cloud_pgw_success[1],cloud_pgw_success[2]]]


ret = []
call, sms, data = [],[],[]
call2, sms2, data2 = [],[],[]
t = []
ret = np.array([[0,0,0,0,0,0],[0,0,0,0,0,0]])
for i in range(0,5):
	nodes = (i*3)+10
	multiplier = (2)
	for i in range(0,5):
		ret = ret + np.array(simulate(nodes, nodes, multiplier))
	ret = ret/5
	t.append(nodes)
	
	call.append(ret[0][0]/(ret[0][3]+ret[0][0]))
	sms.append(ret[0][1]/(ret[0][4]+ret[0][1]))
	data.append(ret[0][2]/(ret[0][5]+ret[0][2]))

	
	call2.append(ret[1][0]/(ret[1][3]+ret[1][0]))
	sms2.append(ret[1][1]/(ret[1][4]+ret[1][1]))
	data2.append(ret[1][2]/(ret[1][5]+ret[1][2]))

#

plt.plot(t,call,'r-',label="VCE")
plt.plot(t,call2,'b-',label = "CCE")
plt.plot(t,sms,'r--',label="VSE")
plt.plot(t,sms2,'b--',label="CSE")
plt.plot(t,data,'ro-',label="VDE")
plt.plot(t,data2,'bo-',label="CDE")
#plt.ylim(0,0.2)
#plt.xlim(10,15)
plt.xlabel("Number of Nodes")
plt.ylabel("Failure Rate")
plt.legend()
plt.savefig('call-gca-cca-constant-failure-rate')

plt.figure()

ret = []
call, sms, data = [],[],[]
call2, sms2, data2 = [],[],[]
t = []
ret = np.array([[0,0,0,0,0,0],[0,0,0,0,0,0]])
for i in range(0,5):
	nodes = (i*3)+10
	multiplier = 2*(i+5)
	for i in range(0,5):
		ret = ret + np.array(simulate(nodes, nodes, multiplier))
	ret = ret/5
	t.append(nodes)
	
	call.append(ret[0][0]/(ret[0][3]+ret[0][0]))
	sms.append(ret[0][1]/(ret[0][4]+ret[0][1]))
	data.append(ret[0][2]/(ret[0][5]+ret[0][2]))

	
	call2.append(ret[1][0]/(ret[1][3]+ret[1][0]))
	sms2.append(ret[1][1]/(ret[1][4]+ret[1][1]))
	data2.append(ret[1][2]/(ret[1][5]+ret[1][2]))

#

plt.plot(t,call,'r-',label="VCE")
plt.plot(t,call2,'b-',label = "CCE")
plt.plot(t,sms,'r--',label="VSE")
plt.plot(t,sms2,'b--',label="CSE")
plt.plot(t,data,'ro-',label="VDE")
plt.plot(t,data2,'bo-',label="CDE")
#plt.ylim(0,0.2)
#plt.xlim(10,15)
plt.xlabel("Number of Nodes")
plt.ylabel("Failure Rate")
plt.legend()
plt.savefig('call-gca-cca-varying-failure-rate')


