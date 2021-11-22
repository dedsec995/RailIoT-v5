import requests
import json
import sensorprocess
from time import sleep
from databasemanager import read, write

	
def dataprocess(message, sensorinfo):
	altitude = float(message['last_Alt'])
	latitude = float(message['last_Lat'])
	longitude = float(message['last_Lon'])

	acc_x = float(sensorinfo['ACC']['ACC_X'])
	acc_y = float(sensorinfo['ACC']['ACC_Y'])

	acc_x_base = float(sensorinfo['ACC']['ACC_X_BASE'])
	acc_y_base = float(sensorinfo['ACC']['ACC_Y_BASE'])


	moi_base = float(sensorinfo['MOI']['MOI_BASE'])
	moi_value = float(sensorinfo['MOI']['MOI'])


	fle_base = float(sensorinfo['FLEX']['FLEX_BASE'])
	fle_value = float(sensorinfo['FLEX']['FLEX'])

	setid = message['last_SetId']


	acc_status = sensorprocess.accelerometer(acc_x,acc_y)
	moi_status = sensorprocess.moisture(moi_value)
	fle_status = sensorprocess.flex(fle_value)
	zonestatus = sensorprocess.slideindex(acc_status[0],acc_status[1],moi_status,fle_status)


	data_out =[{"measurement": 'logicoutput', "tags":{"LOCID":setid},
			"fields": {"SetId": setid,"Lat": latitude, "Alt": altitude, "Lon": longitude,"ACCX_Status": acc_status[0], "ACCY_Status": acc_status[1], "Moi_Status": moi_status, "Fle_Status": fle_status, "Metric": zonestatus}
				}]

	return data_out

if __name__ == "__main__":

	while True:

		try:
		
			message = read()  #fetches the last row from database
			
			sensorinfo = json.loads(message['last_SensorInfo'])

			write_data = dataprocess(message, sensorinfo)

			write(write_data) # writes processed data to database
			
			for j in range(450):
				sleep(1)

		except:
			print("Error")
			sleep(2)
