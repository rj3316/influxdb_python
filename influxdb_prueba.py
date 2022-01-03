# Import the stuff we need
# pip install influxdb
# pip install rich

# Setup database
from influxdb import InfluxDBClient
from datetime import datetime

from time import sleep

from rich import print

# Setup database
host = 'localhost'
port = 8086
user ='root'
password = 'hiru'
db_req = 'influx_python'

client = InfluxDBClient(host, port, user, password)
print(f"Client: {client}")

db = None
for db_dict in client.get_list_database():
    if db_req == db_dict['name']:
        db = db_req
        break

if not db is None:
    client.switch_database(db)

    # Show databases:
    print("\nDatabases:")
    for i, db in enumerate(client.get_list_database()):
        print(f" - {db['name']}")

    print(f"\nMeasurements: {client.get_list_measurements()}")    

    json = []
    data = {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west",
            },
            "time": datetime.utcnow(),
            "fields": {
                "Float_value": 0.0,
                "Int_value": 0,
                "String_value": "Empty",
                "Bool_value": False,
            }
        }
    json.append(data)

    
    # # Writing points
    # client.write_points(json)



    for i in range(5):
        json = []
        data = {
                "measurement": "cpu_load_short",
                "tags": {
                    "host": "server01",
                    "region": "us-west",
                },
                "time": datetime.now(),
                "fields": {
                    "Float_value": 2.1 * i,
                    "Int_value": 11 * i,
                    "String_value": f"Zenbakia {i}a da",
                    "Bool_value": i%2==0,
                }
            }
   
        json.append(data)
        client.write_points(json)


    # for i in json:
    #     print(i)



    print(f"Measurements: {client.get_list_measurements()}")

    query = 'select * from cpu_load_short;'


    bind_params = {'host': 'server01'}

    result = client.query(query)
    print("\nData: Float_value")
    for i in result:
        for j in i:
            print(j)



else:
    print("\nCannot use this database...")