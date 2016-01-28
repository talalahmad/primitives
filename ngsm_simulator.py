# ********
# channel = 1 and number_bw_detection length = 616
# min = 1 and max = 146 and avg = 1.000000
# ********
# channel = 16 and number_bw_detection length = 0
# ********
# channel = 22 and number_bw_detection length = 1
# min = 115 and max = 115 and avg = 115.000000
# ********
# channel = 45 and number_bw_detection length = 74
# min = 1 and max = 30 and avg = 3.000000
# ********
# channel = 48 and number_bw_detection length = 1
# min = 4283 and max = 4283 and avg = 4283.000000
# ********
# channel = 52 and number_bw_detection length = 73
# min = 1 and max = 18 and avg = 2.000000
# ********
# channel = 59 and number_bw_detection length = 29
# min = 1 and max = 7 and avg = 2.000000
# ********
# channel = 89 and number_bw_detection length = 122
# min = 1 and max = 21 and avg = 2.000000
# ********
# channel = 95 and number_bw_detection length = 330
# min = 1 and max = 84 and avg = 2.000000
# [['2015-09-08 19:53:12.497599', '-0.001', 4283], ['2015-09-09 06:27:33.075069', '1', 1], ['2015-09-09 06:27:33.298832', '5', 1], ['2015-09-09 06:27:33.419019', '7', 1], ['2015-09-09 06:27:33.552476', '4', 1], ['2015-09-09 06:27:33.656073', '3', 2], ['2015-09-09 06:27:33.871871', '2', 1], ['2015-09-09 06:27:33.977863', '-0.001', 2012]]

# channel = 1, reports per minute = 0.375023 
# channel = 16, reports per minute = 0.015093 
# channel = 22, reports per minute = 0.239184 
# channel = 45, reports per minute = 1.137980 
# channel = 48, reports per minute = 0.090931 
# channel = 52, reports per minute = 0.748203 
# channel = 59, reports per minute = 0.417339 
# channel = 89, reports per minute = 0.385939 
# channel = 95, reports per minute = 0.727343

maximum_packets_needed = 115 
our_rate = 1.137980
ngsm_rate = 0.090931 
our_users = 2
ngsm_users = 2 

time_taken_by_us = maximum_packets_needed/our_rate
time_taken_by_ngsm = maximum_packets_needed/ngsm_rate

print "time taken by us:%f and time taken by ngsm:%f" %(time_taken_by_us,time_taken_by_ngsm)