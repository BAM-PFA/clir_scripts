'''
Put this script in the directory containing the directories to be renamed
Also include a csv (no headers!) of
	tape number => record ID
in the same dir, named 'record_ids.csv'

the target dirs are all 1-level....
'''
import csv
import os
import re
import shutil

def restructure(new_dir):
	contents = [os.path.join(new_dir,x) for x in os.listdir(new_dir)]
	print(contents)
	for _file in contents:
		if any([x in _file for x in ["_UC.","_AC."]]):
			print(_file)
			os.remove(_file)
	
	doc_dir = os.path.join(new_dir,'documentation')
	print(doc_dir)
	os.mkdir(doc_dir)

	contents = [os.path.join(new_dir,x) for x in os.listdir(new_dir)]
	print(contents)
	for _file in contents:
		if not _file.endswith('_PM.wav'):
			shutil.move(_file,doc_dir)

def rename(target, record_ids):
	print("this is the target dir:"+target)
	try:
		tape_number = re.match(r".*(bampfa_)(\d+(A|B|C|D|E)*)(.*)", target).group(2)
	except:
		tape_number = None

	if tape_number and tape_number in record_ids:
		print("tape_number:"+tape_number)
		record_id = record_ids[tape_number]
		for _file in os.listdir(target):
			current_path = os.path.join(target,_file)			
			new_base = _file.replace(
				'bampfa_{}'.format(tape_number),
				'bampfa-audio_{}'.format(record_id)
				)
			new_path = os.path.join(target,new_base)
			print(new_path)
			os.rename(current_path, new_path)

		new_dir = target.replace(
			'bampfa_{}'.format(tape_number),
			'bampfa-audio_{}'.format(record_id)
			)
		os.rename(target, new_dir)

		restructure(new_dir)

		shutil.move(new_dir, '../ready')

	else:
		pass

def main():
	targets = [os.path.abspath(path) for path in os.listdir('.') if os.path.isdir(path)]
	record_ids = {}
	with open('record_ids.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			record_ids[row[0]] = row[1]

	for target in targets:
		rename(target, record_ids)

if __name__ == "__main__":
	main()
