import rasiberryPiGPIOEquiptAPI.DAO as dao
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import INTERFACE as INTERFACE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_FUCNTION as PIN_FUCNTION
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_MODE as PIN_MODE

def createLEDDeviceInfo():
  ledDevice = dao.addDevice(deviceName = 'LED', deviceType = 'LED', deviceInCategory = '发光二极管', deviceInterfaceType = INTERFACE['GPIO'])
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
  dht22Device = dao.addDevice(deviceName = '温湿传感器DHT22', deviceType = 'DHT22', deviceInCategory = '温度湿度传感器', deviceInterfaceType = INTERFACE['GPIO'])
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

def createBMP180DeviceInfo():
  bmp180Device = dao.addDevice(deviceName = '气压传感器BMP180', deviceType = 'BMP180', deviceInCategory = '气压传感器', deviceInterfaceType = INTERFACE['I2C'], i2cAddress=0x77)
  deviceId = bmp180Device.id
  
  pinList = []
  GNDPin = {
    'pinMode': None, 
    'pinFunction': PIN_FUCNTION['GND']
  }
  VCCPin = {
    'pinMode': None, 
    'pinFunction': PIN_FUCNTION['3V']
  }
  SDAPin = {
    'pinMode': PIN_MODE['I2C'], 
    'pinFunction': PIN_FUCNTION['SDA']
  }
  SDLPin = {
    'pinMode': PIN_MODE['I2C'], 
    'pinFunction': PIN_FUCNTION['SDL']
  }
  pinList.append(GNDPin)
  pinList.append(VCCPin)
  pinList.append(SDAPin)
  pinList.append(SDLPin)
  dao.addDevicePin(deviceId, pinList)

def run():
  print('init database')
  if (len(dao.getDeviceByType('LED')) == 0):
    createLEDDeviceInfo()
  if (len(dao.getDeviceByType('DHT22')) == 0):
    createDHT22DeviceInfo()
  if (len(dao.getDeviceByType('BMP180')) == 0):
    createBMP180DeviceInfo()