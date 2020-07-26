import time
import rtmidi
import json


"""
hello Aslan!

You should set this up to run shortly after running the ruby code.

To run it, you'll need to first run this to install a dependency

> pip install python-rtmidi

then every time in the future you should just be able to run:
> python sosimidirunner.py

This script takes the data from the website, converts it to midi,
and then outputs it to every midi port. If you want to send it
to one midi port, then set `sendToOne` to be True.

The script should run "forever", and you can kill it with pkill or command c
"""

import urllib.request
import urllib.parse


url = 'https://eartalk.org/otherProjects/positions/position_1.json'


sendToOne = False
sendToCustom = "sounds.pink"



midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

midiout.open_virtual_port(sendToCustom)

# find all availiable output ports and open a connection to all of them
print(available_ports)

allPorts = []
allPorts.append(midiout)

if available_ports:
	for i in range(len(available_ports)):
		outputPort = rtmidi.MidiOut()
		outputPort.open_port(i)
		allPorts.append(outputPort)

# now start the big loop
with midiout:
	while True:
		try:
			# request and parse the json file from the url
			f = urllib.request.urlopen(url)
			res = f.read().decode('utf-8')
			positionData = json.loads(res)

			# pull the data we want out of the midi file
			dp1 = round(positionData['left_elbow_angle'])
			dp2 = round(positionData['right_elbow_angle'])
			dp3 = round(positionData['left_arm_angle'])
			dp4 = round(positionData['right_arm_angle'])
			
			# print it for good measure so we can see what is going on
			print(dp1);
			print(dp2);
			print(dp3);
			print(dp4);

			# plop it all into a list
			controlUpdate = [
				[176,14,dp1], # in this message, 176 specifies control data,
				[176,15,dp2], # and 14-17 represents the control channel
				[176,16,dp3],
				[176,17,dp4]
			]
			# for each message in the list, send it.
			for message in controlUpdate:
				if sendToOne:
					# if we only are sending it to the first availiable port
					allPorts[0].send_message(message)
					time.sleep(0.01)
				else:
					#else, we loop through all ports and send the message to all of them.
					for outputPort in allPorts:
						outputPort.send_message(message)
						time.sleep(0.01)
			time.sleep(0.02)
		except:
			pass

del midiout