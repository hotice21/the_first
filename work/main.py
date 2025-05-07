from OOP_work import *
from flask import *
import os,json,shutil
#init
app=Flask(__name__)
hub=SmartHomeHub()
data='data.json'
#api
@app.route('/add',methods=['POST'])
def add_device():
    try:
        devices=request.get_json()
        report=""
        if not devices:
            return 'there is not json file 400'
        with open(data,"r") as fs:
            old_date=json.load(fs)
        for device in devices["hub"]:
            report+=hub.controller.add_device(device)+"\n"
            old_date["hub"].append(device)
        with open(data,"w") as f:
            json.dump(old_date,f,indent=4)
        return report
    except FileNotFoundError:
        return "error: not find file"
    except json.JSONDecodeError:
        return "error: unable to parse the file as valid JSON"
    except Exception as e:
        return str(e)+" 400"
@app.route('/total_amount',methods=['GET'])
def total_amount():
    return str(hub.controller.total_amount())
@app.route('/remove',methods=['POST'])
def remove_device():
    try:
        devices=request.get_json()
        if str(devices['password'])!='114514':
            return 'fail to connect with correct password'
        with open(data,"r") as fs:
            old_date=json.load(fs)
        ids=devices["id"]
        success=""
        error=""
        for _id in ids:
            if _id in hub.controller.devices:
                hub.controller.remove_device(_id)
                for num,device in enumerate(old_date["hub"]):
                    if _id in device:
                        del old_date["hub"][num]
                        break
                success+=str(_id)+" "
            else:
                error+=f"{_id} is not exist\n"
        with open(data,"w") as f:
            json.dump(old_date,f)
        return success+"is deleted\n"+error
    except FileNotFoundError:
        return "error: not find file"
    except json.JSONDecodeError:
        return "error: unable to parse the file as valid JSON"
    except Exception as e:
        return str(e)+' 400'
@app.route('/list',methods=['GET'])
def list_devices():
    return hub.controller.list_devices()
@app.route('/execute/<string:device_id>',methods=['GET'])
def execute_command(device_id):
    try:
        command=request.args.get("command")
        return hub.controller.execute_command(device_id,command)
    except Exception as e:
        return str(e)+"400"
@app.route('/display_status',methods=['GET'])
def display_status():
    return hub.display_status()
@app.route('/total_energy_usage',methods=['GET'])
def total_energy_usage():
    return str(hub.total_energy_usage())
if __name__=='__main__':
    #copying
    shutil.copy(data,"./old data/")
    #loading
    if not os.path.exists('./data.json'):
        with open(data,'w') as fs:
            json.dump({"hub":[]},fs,indent=4)
    else:
        with open(data,'r') as fs:
            datas=json.load(fs)
            for d in datas["hub"]:
                hub.controller.add_device(d)
    #run
    app.run(debug=True)