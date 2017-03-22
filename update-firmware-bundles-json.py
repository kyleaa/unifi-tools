#!/usr/bin/python

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
   
json_file = 'bundles.json' 

import os
import os.path

# Set the working directory
while True:
	dir_set = False
	print 'Select unifi firmware directory:'
	print ' 1) /usr/lib/unifi/dl/firmware'
	print ' 2) .'
	print ' 3) custom path'
	input = raw_input('Choice: ')

	if input == '1':
		new_path = '/usr/lib/unifi/dl/firmware'
	elif input == '2':
		new_path = '.'
		dir_set = True
	elif input == '3':
		new_path = raw_input('Specify path: ')
	else:
		print bcolors.FAIL + bcolors.BOLD + 'Invalid choice\n' + bcolors.ENDC
		continue
	
	if new_path != '.':
		try:
			os.chdir(new_path)
			dir_set = True
		except:
		  print bcolors.FAIL + bcolors.BOLD + "The provided directory does not exist \n" + bcolors.ENDC
		  continue

	if dir_set and os.path.isfile(json_file):
		break
	elif dir_set:
	  print (bcolors.FAIL + bcolors.BOLD + "Expected json file %s was not found. Select another directory.\n" + bcolors.ENDC) % json_file
	  
	  
	
	
    

f = open(json_file,'r')

import json
data = json.load(f)
f.close()
#print json.dumps(data,sort_keys=True, indent=4, separators=(',',': '))

print (bcolors.HEADER + "\nLoaded %s" + bcolors.ENDC ) % json_file
summary = []

# loop through the hardware models
import os
for model in data:
  if not "path" in data[model]:
    continue
  display = data[model]['display']
  path = data[model]['path']
  version = data[model]['version']

  print ( bcolors.BOLD + '\n\nModel %s:%s, version %s' + bcolors.ENDC ) % (model, display, version)
   
  (firmware_dir, tmp) = path.split('/',1)
  
  model_dirs = []
  
  # check for updated firmware files
  for root, dirs, files in os.walk(firmware_dir):
    for (num,name) in enumerate(sorted(dirs)):
      selected = '*' if (name == version) else ''
      print '  %s) %s %s' % (num+1,name,selected)
      model_dirs.append(name)
  
  if len(model_dirs) == 0:
    print bcolors.FAIL  + '  No firmware located in directory %s' + bcolors.ENDC % firmware_dir
    new_version = version
  elif len(model_dirs) == 1:
    # No need to prompt, use the one
    new_version = model_dirs[0]
    if not new_version == version:
	  summary.append(' %s [%s] updated from version %s to %s' % ( display, model, version, new_version) )
    print bcolors.WARNING  + '  No additional firmware located, no change made' + bcolors.ENDC
  else:
    response = raw_input("\n  Select new firmware version [%s]: " % version)
    new_version = version if (response == '') else model_dirs[int(response)-1]
    if new_version == version:
	  print bcolors.WARNING  + '  No change made' + bcolors.ENDC
    else:
	  print (bcolors.OKGREEN + '  Updated firmware to %s' + bcolors.ENDC) % new_version
	  summary.append(' %s [%s] updated from version %s to %s' % ( display, model, version, new_version) )
  
  data[model]['version'] = new_version
  data[model]['path'] = path.replace(version,new_version)
  
if len(summary) == 0:
  # Nothing to do
  print bcolors.BOLD + bcolors.WARNING + 'Nothing to do, exiting ...' + bcolors.ENDC
  import sys
  sys.exit()

print
print bcolors.OKBLUE + bcolors.BOLD + 'SUMMARY OF CHANGES:' + bcolors.ENDC
for message in summary:
  print bcolors.OKBLUE + message + bcolors.ENDC
  
if raw_input("\n Write output to file? (y/n) [n] ") == 'y':
  import datetime
  datestring = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  print "copying %s to %s.%s" % (json_file,json_file,datestring)
  import shutil
  shutil.copyfile(json_file, json_file + '.' + datestring)
  
  print "writing new %s file" % json_file
  with open(json_file, 'w') as outfile:
    json.dump(data, outfile)
  

  
