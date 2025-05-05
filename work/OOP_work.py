import abc
from datetime import datetime
class Device(abc.ABC):
    def __init__(self, device_id, name, energy_usage=0):
        self._device_id = device_id
        self._name = name
        self._status = 'off'
        self._energy_usage = energy_usage
    def get_id(self):
        return self._device_id
    def get_name(self):
        return self._name
    def get_status(self):
        return self._status
    def get_energy_usage(self):
        return self._energy_usage
    def switch(self,command):
        if command=="on":
            self._status="on"
        elif command=="off":
            self._status="off"
        else:
            return "the command is not correct"
        return f'{self._name} has been turn {command}'
    def reset_energy_usage(self,new_energy_usage):
        self._energy_usage=new_energy_usage
        return f"the energy usage of name:{self._name} is changed to {new_energy_usage}"
    @abc.abstractmethod
    def __str__(self):
        return f"Device: {self._name},ID: {self._device_id}, Status: {self._status}, Energy Usage: {self._energy_usage}kWh"

class Light(Device):
    def __init__(self, device_id, name, energy_usage=0,brightness=100):
        super().__init__(device_id,name,energy_usage)
        self._brightness=brightness
    def get_brightness(self):
        return self._brightness
    def reset_brightness(self,new_brightness):
        self._brightness=new_brightness
        return f"the brightness of name:{self._name} is changed to {new_brightness}"
    def __str__(self):
        return f"Device: {self._name},ID: {self._device_id}, Status: {self._status}, Energy Usage: {self._energy_usage}kWh, Brightness: {self._brightness}"

class Thermostat(Device):
    def __init__(self, device_id, name, energy_usage=0,temperature=22):
        super().__init__(device_id,name,energy_usage)
        self._temperature=temperature
    def get_temperature(self):
        return self._temperature
    def reset_temperature(self,new_temperature):
        self._temperature=new_temperature
        return f"the temperature of name:{self._name} is changed to {new_temperature}"
    def __str__(self):
        return f"Device: {self._name},ID: {self._device_id}, Status: {self._status}, Energy Usage: {self._energy_usage}kWh, Temperature: {self._temperature}"

class Camera(Device):
    def __init__(self, device_id, name, energy_usage=0,resolution='1080p',angle=0):
        super().__init__(device_id,name,energy_usage)
        self._resolution=resolution
        self._angle=angle
    def get_resolution(self):
        return self._resolution
    def reset_resolution(self,new_resolution):
        self._resolution=new_resolution
    def __str__(self):
        return f"Device: {self._name},ID: {self._device_id}, Status: {self._status}, Energy Usage: {self._energy_usage}kWh, Resolution: {self._resolution}"

class Fridge(Device):
    """the temperature is in degree centigrad"""
    def __init__(self,device_id,name,energy_usage=0,high_t=5,low_t=-10,stage_status:dict[int]=int):
        super().__init__(device_id,name,energy_usage)
        self._stage_status=stage_status
        self._high_t=high_t
        self._low_t=low_t
    def change_temperature(self,stage,temperature):
        if stage in self._stage_status:
            if self._low_t<=temperature<=self._high_t:
                self._stage_status[stage]=temperature
            else:
                return 'the temperature is out of the limit'
        else:
            return "the fridge has not this stage"
    def __str__(self):
        stage_status=''
        for stage,temperature in self._stage_status.items():
            stage_status+=f"{stage}--{temperature}\t"
        return (f"Device: {self._name},ID: {self._device_id}, Status: {self._status}, \nEnergy Usage: {self._energy_usage}kWh, highest temperature: {self._high_t}"
                f"lowest temperature: {self._low_t}, \neach stage: {stage_status}")

class DeviceController:
    def __init__(self):
        self.devices = {}
    #give the amount in the registered devices
    def total_amount(self):
        return len(self.devices)
    #add form: dict:{"device":device,"name":name,"id":id,"energy_usage"=energy_usage} + **kwargs
    def add_device(self, info_device:dict):
        try:
            device=info_device["device"].lower()
            _id=info_device["id"]
            if _id in self.devices:
                return "this id has been created"
            eu=info_device["energy_usage"] if "energy_usage" in info_device else 0
            if device=="device":
                self.devices[_id]=Device(device_id=_id,name=info_device["name"],energy_usage=eu)
            elif device=="fridge":
                h_t=info_device["high_temperature"] if "high_temperature" in info_device else 5
                l_t=info_device["low_temperature"] if "low_temperature" in info_device else -10
                s_s=info_device["stage_status"]
                self.devices[_id] = Fridge(device_id=_id, name=info_device["name"], energy_usage=eu,high_t=h_t,low_t=l_t,stage_status=s_s)
            elif device=="camera":
                reso=info_device['resolution'] if 'resolution' in info_device else '1080p'
                angle=info_device["angle"] if 'angle' in info_device else 0
                self.devices[_id] = Camera(device_id=_id, name=info_device["name"], energy_usage=eu,resolution=reso,angle=angle)
            elif device=="light":
                self.devices[_id] = Light(device_id=_id, name=info_device["name"], energy_usage=eu,brightness=info_device['brightness'])
            elif device=="thermostat":
                tem=info_device["temperature"] if 'temperature' in info_device else 22
                self.devices[_id] = Thermostat(device_id=_id, name=info_device["name"], energy_usage=eu,temperature=tem)
            else:
                return Exception("this device is not exist ")
            return f"{device}:{info_device['name']} id:{_id} has been adding"
        except Exception as e:
            return str(e)+"\nfail to add device"
    #remove device  if given ID is not exist raise error
    def remove_device(self, device_id):
        if device_id in self.devices.keys():
            del self.devices[device_id]
        else:
            return KeyError("this device id is not exist")
    #output the device name and return the list of id
    def list_devices(self):
        info=""
        for device in self.devices.values():
            info+=device.__str__()+"\n"
        return info
    #switch device method
    def execute_command(self, device_id :str, command :str):
        try:
            name = self.devices[device_id]
            return name.switch(command)
        except Exception as e:
            return str(e)

# Smart Home Hub (Singleton)
class SmartHomeHub:
    _instance = None
    #to ensure that all objects share one and the same class
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmartHomeHub, cls).__new__(cls)
            cls._instance.controller = DeviceController()
        return cls._instance
    #if the datetime is the same to the given time, switch the device
    def schedule_task(self, device_id, command, time):
        pass
    #output all device name and their status
    def display_status(self):
        sum_status=""
        for device in self.controller.devices.values():
            sum_status+=f"{device.get_name()}:{device.get_status()}"
        return sum_status
    #return the total of all energy usage
    def total_energy_usage(self):
        total_usage=0
        for device_id in self.controller.devices.keys():
            total_usage+=self.controller.devices[device_id].get_energy_usage()
        return total_usage
#sample
if __name__ == "__main__":
    hub = SmartHomeHub()
    hub.controller.add_device({"name":"living room right light","id":"L1","device":"light","brightness":100,"energy_usage":3})
    hub.controller.add_device({"name": "living room left light", "id": "L2", "device": "light", "brightness": 100, "energy_usage": 3})
    hub.controller.add_device({"name": "kitchen fridge", "id": "F1", "device": "fridge","energy_usage": 100,"stage_status":{1:2,2:-3,3:-5},"high_temperature":4,"low_temperature":-7})
    hub.controller.add_device({"name": "living Camera", "id": "C1", "device": "camera", "energy_usage": 3,"resolution":"2k","angle":2})
    hub.controller.add_device({"name": "Thermostat", "id": "T1", "device": "thermostat", "energy_usage": 200,"temperature":24})
    hub.controller.add_device({"name":"device","device":"device","id":"D1","energy_usage":5})
    hub.controller.add_device({"name": "device", "device": "device", "id": "D1", "energy_usage": 5})
    print(hub.display_status())
    print(hub.controller.list_devices())
    print(hub.controller.remove_device("D1"))
    print(hub.controller.list_devices())
    hub.controller.execute_command("L1","on")
    print(hub.controller.total_amount())
    print(hub.total_energy_usage())