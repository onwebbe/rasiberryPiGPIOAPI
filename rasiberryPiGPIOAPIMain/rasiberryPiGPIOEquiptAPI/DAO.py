from rasiberryPiGPIOEquiptAPI.models import DeviceInfo
from rasiberryPiGPIOEquiptAPI.models import DevicePin
from rasiberryPiGPIOEquiptAPI.models import PiDeviceInfo
from rasiberryPiGPIOEquiptAPI.models import PiDevicePin
from rasiberryPiGPIOEquiptAPI.models import DeviceData
from rasiberryPiGPIOEquiptAPI.models import DeviceDataHistory


def addDevice(deviceName, deviceType, deviceInCategory, deviceInterfaceType, i2cAddress = ''):
  device = DeviceInfo(deviceName = deviceName, deviceType = deviceType, deviceInCategory = deviceInCategory, deviceInterfaceType = deviceInterfaceType, i2cAddress = i2cAddress)
  device.save()
  return device

def getDevices():
  return DeviceInfo.objects.all()

def getDeviceByName(name):
  return DeviceInfo.objects.filter(deviceName = name)

def getDeviceByType(type):
  return DeviceInfo.objects.filter(deviceType = type)

def getDeviceById(id):
  return DeviceInfo.objects.get(id = id)

def addDevicePin(deviceId, pinList): # {'pinMode': '', 'pinFunction': ''}
  pinResultList = []
  for pinObjData in pinList:
    pinMode = pinObjData['pinMode'] if pinObjData['pinMode'] is not None else -1
    pinFunction = pinObjData['pinFunction'] if pinObjData['pinFunction'] is not None else -1
    pin = DevicePin(deviceID = deviceId, pinMode = pinMode, pinFunction = pinFunction)
    pin.save()
    pinResultList.append(pin)
  return pinResultList

def getDevicePinById(id):
  return DevicePin.objects.get(id = id)

def getDevicePinByDeviceId(deviceId):
  return DevicePin.objects.filter(deviceID = deviceId)

def addPiDevice(deviceId, name):
  device = PiDeviceInfo(deviceID = deviceId, piDeviceName = name)
  device.save()
  return device

def updatePiDevice(piDeviceId, name):
  PiDeviceInfo.objects.filter(id = piDeviceId).update(piDeviceName = name)
  return PiDeviceInfo.objects.get(id = piDeviceId)

def deletePiDevice(piDeviceId):
  PiDeviceInfo.objects.filter(id = piDeviceId).delete()
  pass

def getPiDeviceById(piDeviceId):
  return PiDeviceInfo.objects.get(id = piDeviceId)

def getPiDevices():
  return PiDeviceInfo.objects.all()

def getPiDeviceByDeviceId(deviceId):
  return PiDeviceInfo.objects.filter(deviceID = deviceId)

def addPiDevicePin(piDeviceId, pinDataList):
  pinList = []
  for pinData in pinDataList:
    pinBoardId = pinData['pinBoardId']
    devicePinID = pinData['devicePinID']
    pinValue = pinData['value'] if pinData['value'] is not None else ''
    pin = None
    if (checkPiDevicePinExists(piDeviceId, devicePinID)): # if exists update
      pin = PiDevicePin.objects.filter(piDeviceID = piDeviceId, devicePinID = devicePinID).update(pinBoardID = pinBoardId, pinValue = pinValue)
      pinList.append(PiDevicePin.objects.filter(piDeviceID = piDeviceId, devicePinID = devicePinID)[0])
    else: #if not exists add new
      pin = PiDevicePin(piDeviceID = piDeviceId, pinBoardID = pinBoardId, devicePinID = devicePinID, pinValue = pinValue)
      pin.save()
      pinList.append(pin)
  return pinList

def getPiDevicePinById(piDevicePinId):
  return PiDevicePin.objects.get(id = piDevicePinId)

def getPiDevicePinByPiDeviceId(piDeviceId):
  return PiDevicePin.objects.filter(piDeviceID = piDeviceId)

def checkPiDevicePinExists(piDeviceId, devicePinId):
  return len(PiDevicePin.objects.filter(piDeviceID = piDeviceId, devicePinID = devicePinId)) > 0

def updateDevicePinBoardId(piDevicePinId, boardId):
  updatedPin = PiDevicePin.objects.filter(id = piDevicePinId).update(pinBoardID = boardId)
  return updatedPin

def addDeviceData(deviceId, dataName, value):
  data = DeviceData(deviceID = deviceId, deviceDataName = dataName, deviceDataValue = value)
  dataHistory = DeviceDataHistory(deviceID = deviceId, deviceDataName = dataName, deviceDataValue = value)
  data.save()
  dataHistory.save()

def updateDeviceData(deviceId, dataName, value):
  DeviceData.objects.filter(deviceID = deviceId, deviceDataName = dataName).update(deviceDataValue = value)
  dataHistory = DeviceDataHistory(deviceID = deviceId, deviceDataName = dataName, deviceDataValue = value)
  dataHistory.save()

def checkPinIsAvailable(pinBoardID):
  if (len(PiDevicePin.objects.filter(pinBoardID = pinBoardID)) > 0):
    return False
  else:
    return True

