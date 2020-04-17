from rasiberryPiGPIOEquiptAPI.models import DeviceInfo
from rasiberryPiGPIOEquiptAPI.models import PiDeviceInfo
from rasiberryPiGPIOEquiptAPI.models import PiDevicePin
from rasiberryPiGPIOEquiptAPI.models import DeviceData
from rasiberryPiGPIOEquiptAPI.models import DeviceDataHistory


def addDevice(deviceName, deviceInterfaceType):
  device = DeviceInfo(deviceName = deviceName, deviceType = '', deviceInterfaceType = deviceInterfaceType)
  device.save()
  return device

def getDevices():
  return DeviceInfo.objects.all()

def addDevicePin(deviceId, pinList): # {'pinMode': '', 'pinFunction': ''}
  pinResultList = []
  for pinObjData in pinList:
    pinMode = pinObjData['pinMode'] if pinObjData['pinMode'] is not None else -1
    pinFunction = pinObjData['pinFunction'] if pinObjData['pinFunction'] is not None else -1
    pin = PiDeviceInfo(deviceID = deviceId, pinMode = pinMode, pinFunction = pinFunction)
    pin.save()
    pinResultList.append(pin)
  return pinResultList

def addPiDevice(deviceId, name):
  device = PiDeviceInfo(deviceID = deviceId, deviceName = '')
  device.save()
  return device

def addPiDevicePin(piDeviceId, pinData):
  pinList = []
  for pinBoardId, pinObjData in pinData.items:
    pinMode = pinObjData['pinMode'] if pinObjData['pinMode'] is not None else -1
    pinFunction = pinObjData['pinFunction'] if pinObjData['pinFunction'] is not None else -1
    pinValue = pinObjData['value'] if pinObjData['value'] is not None else ''
    pin = PiDeviceInfo(deviceID = piDeviceId, pinBoardID = pinBoardId, pinMode = pinMode, pinFunction = pinFunction, pinValue = pinValue)
    pin.save()
    pinList.append(pin)
  return pinList

def updateDevicePinBoardId(piDevicePinId, boardId):
  updatedPin = PiDeviceInfo.objects.filter(id = piDevicePinId).update(pinBoardID = boardId)
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

