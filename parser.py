import re
def parse(f, readings):
	for line in open(f,'r'):
		print line
		answer = re.findall('{[0-9]*:.*[0-9]',line)
		print answer[0]
		ans = answer[0][1:]
		ans = ans.split(', ')
		print ans
		for item in ans:
			broken = item.split(': ')
			key = broken[0]
			value = broken[1]
			print "key = %s and value = %s" %(key,value)
			if key in readings:
				readings[key].append(value)
			else:
				readings[key] = []
				readings[key].append(value)
	return readings;

readings = {}
readings = parse("/home/alfred/WHITESPACES/measurement_report_first_set", readings);
readings = parse("/home/alfred/WHITESPACES/measurement_report_second_set", readings);
readings = parse("/home/alfred/WHITESPACES/measurement_report_final_set", readings);
#print result
print "***************"
for key in sorted(readings):
	sum = 0.0
	for entry in readings[key]:
		if entry[0] is '-':
			sum = sum + 0
		else:
			sum = sum + float(entry)
	print "key = %s and number of readings = %d and sum = %f" %(key, len(readings[key]), sum) 