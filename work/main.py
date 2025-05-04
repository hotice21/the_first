from OOP_work import *
from flask import *
import os,json
app=Flask(__name__)
hub=SmartHomeHub()
data='data.json'
@app.route('/add',methods=['POST'])
def add_device():
    try:
        device=request.get_json()
        if not device:
            return 'there is not json file',400
        hub.controller.add_device(dict(device))
        with open(data,"a"):
            json.load(device)
    except Exception as e:
        return str(e)+"400"
@app.route('/total_amount',methods=['GET',"POST"])
def total_amount():
    return str(hub.controller.total_amount())
@app.route('/remove',methods=['DELETE'])
def remove_device():
    try:
        device=request.json()
        if str(device['password'])!='114514':
            return 'fail to connect with correct password'
        if device['id'] in hub.controller.devices:
            del hub.controller.devices[device["id"]]
        with open(data,"") as f:

    except Exception as e:
        return str(e)+'400'
@app.route('/list',methods=['GET'])
def list_devices():
    return hub.controller.list_devices()
@app.route('/execute',methods=['POST'])
def execute_command(device_id,command):
    return hub.controller.execute_command(device_id,command)
@app.route('/display_status',methods=['GET'])
def display_status():
    return hub.display_status()
@app.route('/total_energy_usage',methods=['GET'])
def total_energy_usage():
    return str(hub.total_energy_usage())
if __name__=='__main__':
    #loading
    if not os.path.exists('./data.json'):
        with open(data,'w') as f:
            json.dump([],f)
    else:
        with open(data,'r') as f:
            datas=json.load(f)
            for data in datas:
                hub.controller.add_device(data)
    app.run(debug=True)