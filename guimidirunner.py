import time
import rtmidi
import json
import urllib.request
import urllib.parse
from tkinter import *

SOUNDS_PINK = 'sounds.pink'
CUSTOM_CODE_NONE = '[NONE]'
CUSTOM_CODE_INVALID = '[INVALID]'
CUSTOM_CODE_CHECKING = '[CHECKING]'

CUSTOM_CODE_ENTERED = CUSTOM_CODE_NONE
CUSTOM_CODE = CUSTOM_CODE_NONE
MIDI_PORT_SELECTED = SOUNDS_PINK

HAS_VALIDATED_CUSTOM_CODE = False


#### MIDI SETUP SECTION

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
midiout.open_virtual_port(SOUNDS_PINK)
# find all availiable output ports and open a connection to all of them
print(available_ports)
allPorts = {}
allPorts[SOUNDS_PINK] = midiout
if available_ports:
	for i in range(len(available_ports)):
		outputPort = rtmidi.MidiOut()
		outputPort.open_port(i)
		allPorts[available_ports[i]] = outputPort
		print(allPorts)
available_ports.insert(0,SOUNDS_PINK)




### THE ACTUAL LOGIC

def fetchJsonFromWeb():
	if(CUSTOM_CODE == CUSTOM_CODE_NONE):
		return {}
	try:
		url = 'https://eartalk.org/otherProjects/positions/position_{0}.json'.format(CUSTOM_CODE)
		f = urllib.request.urlopen(url)
		res = f.read().decode('utf-8')
		positionData = json.loads(res)
		return positionData
	except Exception as e: print(e)

def sendMidiData(jsonOBJ):
	for k in jsonOBJ:
		updateMessage = [176,jsonOBJ[k]['cc'],jsonOBJ[k]['val']]
		allPorts[MIDI_PORT_SELECTED].send_message(updateMessage)
		time.sleep(0.001)


allMidiTableUpdateSVs = {}

gridRowToAddAt = 3
def updateMidiTable(jsonOBJ):
	global gridRowToAddAt
	for k in jsonOBJ:
		if(not k in allMidiTableUpdateSVs):
			sv = StringVar()
			label = Label(master, textvariable=sv).grid(row=gridRowToAddAt,columnspan=2)
			allMidiTableUpdateSVs[k] = sv
		allMidiTableUpdateSVs[k].set("Sending {0} to cc {1}, current value: {2}".format(k, jsonOBJ[k]['cc'],jsonOBJ[k]['val']))
		gridRowToAddAt+=1









##### UI CODE

OPTIONS = available_ports #etc

def updateInformLabel():
	print(custom_code_sv.get())
	CUSTOM_CODE_ENTERED = custom_code_sv.get()
	if(CUSTOM_CODE_ENTERED == ''):
		CUSTOM_CODE = CUSTOM_CODE_NONE
		CUSTOM_CODE_ENTERED = CUSTOM_CODE_NONE
	elif(len(CUSTOM_CODE_ENTERED) < 4 or len(CUSTOM_CODE_ENTERED) > 4):
		CUSTOM_CODE = CUSTOM_CODE_NONE
		CUSTOM_CODE_ENTERED = CUSTOM_CODE_INVALID
	elif(HAS_VALIDATED_CUSTOM_CODE == False):
		# we'll set it and see if it is worth doing.
		CUSTOM_CODE = CUSTOM_CODE_ENTERED;
		CUSTOM_CODE_ENTERED = CUSTOM_CODE_CHECKING
	print(CUSTOM_CODE_ENTERED),
	print(MIDI_PORT_SELECTED)
	if(CUSTOM_CODE_ENTERED == CUSTOM_CODE_NONE or CUSTOM_CODE_ENTERED == CUSTOM_CODE_INVALID):
		v.set("Please enter a 4 digit custom code")	
	elif(CUSTOM_CODE_ENTERED == CUSTOM_CODE_CHECKING):
		v.set("Checking custom code {0}...".format(custom_code_sv.get()))
	else:
		v.set("sending data from {0} to {1}".format(CUSTOM_CODE_ENTERED,MIDI_PORT_SELECTED))

	updateMidiTable({
		"hello": {
			"val":120,
			"cc":10
			}
		})


def OptionMenu_SelectionEvent(event):
	print("wow changing to the new thing")
	print(event);
	MIDI_PORT_SELECTED = event
	updateInformLabel()
	## do something
	pass




master = Tk()
master.title("sounds.pink")
custom_code_sv = StringVar()
v = StringVar()


def UpdateCustomCode(a,b,c):
	HAS_VALIDATED_CUSTOM_CODE = False
	updateInformLabel()
	return True



label0 = Label(master, text="midi output:").grid(row=0)
label1 = Label(master, text="custom code:").grid(row=1)
label2 = Label(master, textvariable=v).grid(row=2,columnspan=2)



custom_code_sv.trace_add("write", UpdateCustomCode)







variable = StringVar(master)
variable.set(OPTIONS[0]) # default value
e = Entry(master, textvariable=custom_code_sv, validate="focusout", validatecommand=UpdateCustomCode)
e.grid(row=1,column=1)

w = OptionMenu(master, variable, *OPTIONS, command=OptionMenu_SelectionEvent)
w.grid(row=0,column=1)

updateInformLabel()

mainloop()















