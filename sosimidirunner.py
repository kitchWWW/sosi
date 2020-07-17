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


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# find all availiable output ports and open a connection to all of them
print(available_ports)
allPorts = []

if available_ports:
	for i in range(len(available_ports)):
		outputPort = rtmidi.MidiOut()
		outputPort.open_port(i)
		allPorts.append(outputPort)

with midiout:
	while True:

		f = urllib.request.urlopen(url)
		res = f.read().decode('utf-8')
		positionData = json.loads(res)
		dp1 = round(positionData['left_elbow_angle'])
		dp2 = round(positionData['right_elbow_angle'])
		dp3 = round(positionData['left_arm_angle'])
		dp4 = round(positionData['right_arm_angle'])
		
		print(dp1);
		print(dp2);
		print(dp3);
		print(dp4);

		controlUpdate = [
			[176,14,dp1],
			[176,15,dp2],
			[176,16,dp3],
			[176,17,dp4]
		]
		for message in controlUpdate:
			if sendToOne:
				allPorts[0].send_message(message)
			else:
				for outputPort in allPorts:
					outputPort.send_message(message)
		time.sleep(0.05)

del midiout