from influxdb import InfluxDBClient

# influxdb details
"""Instantiate a connection to the InfluxDB."""
dbhost = 'localhost'
dbport = 8086
dbuser = 'root'
dbpassword = 'root'
dbname = 'sensordataDB'  #name of the database created

# creating client instance
dbclient = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)
dbclient.create_database(dbname)



def write(data_write):
	dbclient.write_points(data_write)
		

def read():
	return list(dbclient.query('select last(*) from sensordata'))[0][0]


