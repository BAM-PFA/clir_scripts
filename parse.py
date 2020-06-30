import csv
import ast

data = {}
new = {}

fp = '/Users/michael/Desktop/clir_file_mgmt/mp_still-need-perms-parsed.csv'
with open(fp,'r') as x:
	reader = csv.reader(x)
	for line in reader:
		data[line[0]] = {}
		data[line[0]]['dates'] = line[1]
		try:
			data[line[0]]['people'] = ast.literal_eval(line[2])
		except:
			data[line[0]]['people'] = [line[2]]
		try:
			data[line[0]]['titles'] = ast.literal_eval(line[3])
		except:
			data[line[0]]['titles'] = [line[3]]

for k,v in data.items():
	for x in v['people']:
		if not x in new:
			new[x] = {}
			new[x]['dates'] = []
			new[x]['titles'] = []
			new[x]['recording ids'] = []
		new[x]['dates'].append(v['dates'])
		new[x]['recording ids'].append(k)
		for t in v['titles']:
			new[x]['titles'].append(t)

with open('parsed-perm-needers.csv','w+') as f:
	writer = csv.writer(f)
	for k,v in new.items():
		row = [k,v['dates'],v['titles'],v['recording ids']]
		writer.writerow(row)

print(new)
