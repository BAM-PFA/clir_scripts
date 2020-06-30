import csv

to_fix = '/Users/michael/Desktop/clir_file_mgmt/to-fix.csv'
export = '/Users/michael/Desktop/clir_file_mgmt/export-for-fixing-md.csv'
outpath = "fixed.csv"
ids_tofix = {}

with open(to_fix,'r') as t:
	t_reader = csv.DictReader(t)

	for row in t_reader:
		ids_tofix[row['Resource ID(s)']] = row['Audio recording ID']

with open(export,'r') as e:
	e_reader = csv.DictReader(e)
	out = []
	for row in e_reader:
		for k,v in ids_tofix.items():
			if row['Audio recording ID'] == v:
				row['Resource ID(s)'] = k
				out.append(row)

print(out[0].keys())
with open(outpath,'w') as outfile:
	fp = csv.DictWriter(outfile, out[0].keys())
	fp.writeheader()
	fp.writerows(out)
