import rasiberryPiGPIOEquiptAPI.DAO as dao
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import INTERFACE as INTERFACE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_FUCNTION as PIN_FUCNTION
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_MODE as PIN_MODE

def createLEDDeviceInfo():
  ledDevice = dao.addDevice(deviceName = 'LED', deviceType = 'LED', deviceInterfaceType = INTERFACE['GPIO'])
  deviceId = ledDevice.id
  
  pinList = []
  GNDPin = {
    'pinMode': None, 
    'pinFunction': PIN_FUCNTION['GND']
  }
  VPIN = {
    'pinMode': PIN_MODE['OUT'], 
    'pinFunction': PIN_FUCNTION['GPIO']
  }
  pinList.append(GNDPin)
  pinList.append(VPIN)
  dao.addDevicePin(deviceId, pinList)

def createDHT22DeviceInfo():
  dht22Device = dao.addDevice(deviceName = 'DHT22', deviceType = 'DHT22', deviceInterfaceType = INTERFACE['GPIO'])
  deviceId = dht22Device.id
  
  pinList = []
  GNDPin = {
    'pinMode': None, 
    'pinFunction': PIN_FUCNTION['GND']
  }
  VCCPin = {
    'pinMode': None, 
    'pinFunction': PIN_FUCNTION['3V']
  }
  VPIN = {
    'pinMode': PIN_MODE['IN'], 
    'pinFunction': PIN_FUCNTION['GPIO']
  }
  pinList.append(GNDPin)
  pinList.append(VCCPin)
  pinList.append(VPIN)
  dao.addDevicePin(deviceId, pinList)

def run():
  print('init database')
  if (len(dao.getDeviceByName('LED')) == 0):
    createLEDDeviceInfo()
  if (len(dao.getDeviceByName('DHT22')) == 0):
    createDHT22DeviceInfo()