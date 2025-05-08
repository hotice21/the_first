#run when main.py is running
import requests,json,os
url_1='http://127.0.0.1:5000/add'
url_2='http://127.0.0.1:5000/remove'
url_3='http://127.0.0.1:5000/schedule'
url_4='http://127.0.0.1:5000/list'
url_5='http://127.0.0.1:5000/execute/T1?on'
url_6='http://127.0.0.1:5000/total_energy_usage'
add_json={"hub": [{"device": "light", "id": "L2", "name": "bedroom light", "energy_usage": 5, "brightness": 80},
                   {"id": "L1", "name": "bathroom light", "device": "light", "energy_usage": 45, "brightness": 200},
                  {"device": "Thermostat", "id": "T1", "name": "house Thermostat", "energy_usage": 2000,"temperature":24},
                  {"device": "Camera", "id": "C1", "name": "living room camera", "energy_usage": 10, "resolution":"1080p","angle":0 },
                  {"device": "Fridge", "id": "F1", "name": "kitchen", "energy_usage": 200,'stage_status':{1:3,2:0,3:-4}}]}
remove_json={"password":"114514",
             "id":["L1","C1"]}
time_json={"11:00":{"L2":"on"},
           "12:12":{"L2":"off","F1":"on"}}
with open("./test/add.json","rb") as f:
    try:
        print(url_1)
        files = {"file": f}
        respond = requests.post(url_1, data=add_json,files=files)
        print(respond.text)
    except Exception as e:
        print(str(e))
with open("./test/remove.json","rb") as f:
    try:
        print(url_2)
        files = {"file": f}
        respond = requests.post(url_2, data=remove_json, files=files)
        print(respond.text)
    except Exception as e:
        print(str(e))
with open("./test/time.json","rb") as f:
    try:
        print(url_3)
        files = {"file": f}
        respond = requests.post(url_3, data=time_json, files=files)
        print(respond.text)
    except Exception as e:
        print(str(e))
try:
    print(url_2)
    respond=requests.post(url_2,files="./test/remove.json")
    print(respond.text)
except Exception as e:
    print(str(e))
try:
    print(url_3)
    respond=requests.post(url_3,files="./test/time.json")
    print(respond.text)
except Exception as e:
    print(str(e))
try:
    print(url_4)
    respond=requests.get(url_4)
    print(respond.text)
except Exception as e:
    print(str(e))
try:
    print(url_5)
    respond=requests.get(url_5)
    print(respond.text)
except Exception as e:
    print(str(e))
try:
    print(url_6)
    respond=requests.get(url_6)
    print(respond.text)
except Exception as e:
    print(str(e))