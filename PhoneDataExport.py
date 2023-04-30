#!/usr/bin/python3

import dbus
import time
import json
bus = dbus.SystemBus()

phone_data =''
def main():
	global phone_data 
	manager = dbus.Interface(bus.get_object('org.ofono', '/'),
						'org.ofono.Manager')

	modems = manager.GetModems()
	for path, properties in modems:
	#	print("[ %s ]" % (path))
	#	print(path)
		json_properties = json.dumps(properties) 
		json_data = json.loads(json_properties)
	#	print(json_data)
		Name = json_data.get('Name')
		Type = json_data.get('Type')
		Online = json_data.get('Online')
		Serial = json_data.get('Serial')
	#	print(Name)
	#	print(Online)
	#	print(Type)
	#	print(Serial)
	#	if (Online == 0) and (Type == "hardware"):
	#		print("Wrong modem")
		if (Online == 0) and (Type == "hfp"):
		 	State = "Not connected"
		 	Number = "Not connected"
		 	StartTime = "Not connected"
		 	Path = "Not connected"
		 	Phone = "Not connected"
		 	Serial= "Not connected"
		 	phone_data = {'Phone': Phone, 'Serial': Serial, 'State': State, 'Number': Number, 'StartTime': StartTime, 'Path': Path}
		# 	print(Name) 
		#	print(Type) 
		#	print(Online)
		#	print(Serial) 
		if (Online == 1) and (Type == "hfp"):
			Phone = Name
			if "org.ofono.VoiceCallManager" not in properties["Interfaces"]:
				continue
	
			mgr = dbus.Interface(bus.get_object('org.ofono', path),
						'org.ofono.VoiceCallManager')
			try:
				calls = mgr.GetCalls()
				#print("Call Data")
				json_properties_call = json.dumps(calls)
				#print(json_properties_calls)
				path = json_properties_call.split('"', 1)[1].split('"', 1)[0]
				#print(json_properties_path)
				json_properties_call = json_properties_call.split(",", 1)[1].split("}", 1)[0]
				json_properties_call = str(json_properties_call + "}")

				json_data_call = json.loads(json_properties_call)
				State = json_data_call.get('State')
				Number = json_data_call.get('LineIdentification')
				StartTime = json_data_call.get('StartTime')
				Path = path


			except:
				State = "No active calls"
				Number = " "
				StartTime = " "
				Path = " "
					
			phone_data = {'Phone': Phone, 'Serial': Serial, 'State': State, 'Number': Number, 'StartTime': StartTime, 'Path': Path}
		#print(phone_data)
			
if __name__ == '__main__':
    main()
