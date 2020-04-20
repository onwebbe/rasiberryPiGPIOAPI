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

def run():
  print('init database')
  if (len(dao.getDevices()) == 0):
    createLEDDeviceInfo()