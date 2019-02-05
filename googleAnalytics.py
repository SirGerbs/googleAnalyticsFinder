#!/usr/bin/python3
import requests
import sys
import re
import urllib3
import signal

#disable insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#file given on command line
myFile = sys.argv[1]

#loop through file
with open(myFile, 'r') as file:
	#dict to hold Google Analytics IDs
	uaNumbers = []
	for line in file:
		#strip newline from URL
		line = line.rstrip("\r\n")
		print('[*] Checking '+ line)

		#request the page at the domain
		try:
			r = requests.get(line, verify=False, timeout=5)
		except KeyboardInterrupt:
			print('...Exiting...')
			exit(0)
		except:
			print('[!]    Request errored out')

		#regex match "UA-" to see if the page contains google analytics
		p = re.compile('UA-\d[^"|\']*')
		m = p.search(r.text)
		if m is not None:
			print('[!]   Found ' + m.group())

			#add analytics ID to dict if it's not in there yet
			if m.group() not in uaNumbers:
				uaNumbers.append(m.group())

	print("\nThe following unique Google Analytics IDs were found:")
	for id in uaNumbers:
		print(id)
