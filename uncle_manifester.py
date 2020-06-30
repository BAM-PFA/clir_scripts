# go through the MEDIAVAULT folders
# and figure out which assets are already staged
# and posted to IA, which are awaiting staging
# add ia URL as appropriate
#get checksum from mediapreserve XML
# get file modification date to equal the "date last checked" since they were checked on import

# ACCESS  FILENAME
# DIRECT URL TO FILE
# CHECKSUM
# DATE LAST CHECKED
# RESTRICTED? (Y/N)
# COMMENTS ABOUT RESTRICTIONS
# PRESERVATION FILENAME
# PRESERVATION FILE LOCATION

# ./problems/bampfa-audio_00291
# ./problems/bampfa-audio_03389

import csv
import os
import re
import pandas as pd

headers = ['tape_id',
		'ACCESS FILENAME',
		'DIRECT URL TO FILE',
		'CHECKSUM',
		'DATE LAST CHECKED',
		'RESTRICTED? (Y/N)',
		'COMMENTS ABOUT RESTRICTIONS',
		'PRESERVATION FILENAME',
		'PRESERVATION FILE LOCATION']

def manifest():
	manifestpath = 'manifest.csv'

	staged = []
	renaming = []

	folders = ['staged','renaming']

	_items = {}

	for folder in os.listdir('staged'):
		staged.append(folder)
	for folder in os.listdir('renaming'):
		if os.path.isdir(os.path.join('renaming',folder)):
			renaming.append(folder)

	# print(staged)
	# print(renaming)

	for item in staged:
		# each should be a folder name like bampfa-audio_12345/
		item_id = item.replace('bampfa-audio_','')
		item_path = os.path.join('staged',item)
		# print(item_path)
		contents = [x for x in os.listdir(item_path)]
		documentation_path = os.path.join(item_path,'documentation')
		access_files = [x.replace('_PM.wav','_access.mp3') for x in contents if x.endswith('.wav')]
		md5_paths = [os.path.join(documentation_path,x) for x in os.listdir(documentation_path) if x.endswith('md5')]
		md5s = []
		for x in md5_paths:
			with open(x,'r') as f:
				lines = f.readlines()
				m = re.match(r'(.+)(  )(.+)',lines[0]).groups()[0]
				md5s.append(m)
				
		_items[item_id] = {}
		_items[item_id]['tape_id'] = item_id
		_items[item_id]['ACCESS FILENAME'] = access_files
		_items[item_id]['DIRECT URL TO FILE'] = "https://archive.org/details/{}".format(item)
		_items[item_id]['CHECKSUM'] = md5s
		_items[item_id]['DATE LAST CHECKED'] = ' '
		_items[item_id]['RESTRICTED? (Y/N)'] = 'N'
		_items[item_id]['COMMENTS ABOUT RESTRICTIONS'] = ' '
		_items[item_id]['PRESERVATION FILENAME'] = [x for x in os.listdir(item_path) if x.endswith('.wav')]
		_items[item_id]['PRESERVATION FILE LOCATION'] = ["LTO tape storage"]

		# print(_items[item_id])

	for item in renaming:
		# each should be a folder name like bampfa_12345/
		item_id = item.replace('bampfa_','')
		item_path = os.path.join('renaming',item)
		contents = [x for x in  os.listdir(item_path)]
		access_files = ["10.253.22.51:/home/MEDIAVAULT/CLIR_audio/final_masters/staging/"+item+"/"+x for x in contents if x.endswith('mp3')]
		md5_paths = [os.path.abspath(x) for x in contents if x.endswith('wav.md5')]

		_items[item_id] = {}
		_items[item_id]['tape_id'] = item_id
		_items[item_id]['ACCESS FILENAME'] = access_files
		_items[item_id]['DIRECT URL TO FILE'] = " "
		_items[item_id]['CHECKSUM'] = md5s
		_items[item_id]['DATE LAST CHECKED'] = ' '
		_items[item_id]['RESTRICTED? (Y/N)'] = 'Y'
		_items[item_id]['COMMENTS ABOUT RESTRICTIONS'] = 'Item is either awaiting permissions clearance or is complex and needs further treatment/filemanagement in order to ingest.'
		_items[item_id]['PRESERVATION FILENAME'] = [x for x in os.listdir(item_path) if x.endswith('PM.wav')]
		_items[item_id]['PRESERVATION FILE LOCATION'] = ["Enterprise ZFS-enabled Network Attached Storage device (MEDIAVAULT)"]

		# print(_items[item_id])

	with open('manifest.csv','w') as outfile:
		output = csv.DictWriter(outfile,fieldnames=headers)
		output.writeheader()
		#print(_items)
		for k,v in _items.items():
			# print(k)
			print(v)
			output.writerow(v)

def add_checked():
	receipts = 'receipts.csv' # csv of "tape number":"date received"
	manifest = 'manifest.csv' # manifest from above
	man_out = 'manifest_w-date.csv'
	out_rows = []
	with open(manifest,'r') as f:
		manifest_reader = csv.DictReader(f)
		headers = manifest_reader.fieldnames
		# print(headers)
		rdf = pd.read_csv(receipts,index_col=0)
		for row in manifest_reader:
			out_rows.append(row)
			if row['tape_id'] in rdf.index:
				print(row['tape_id'])
				row['DATE LAST CHECKED'] = rdf.loc[row['tape_id']]['date']

	with open(man_out,'w') as f:
		out = csv.DictWriter(f,fieldnames=headers)
		out.writeheader()
		for i in out_rows:
			out.writerow(i)
