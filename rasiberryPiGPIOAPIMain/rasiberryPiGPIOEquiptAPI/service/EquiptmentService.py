import rasiberryPiGPIOEquiptAPI.DAO as dao

def registNewDevice(deviceId, name): #pinDataList [{function: 0, mode: 1}] 
  device = dao.addDevice(deviceId, name)
  pinList = []
  for pinData in pinList:
    # if not regist pin to Pi Board, default to -1
    pinObj = {
      -1: {
        'pinMode': pinData.mode, 
        'pinFunction': pinData.function, 
        'value':''}
    }
    pin = dao.addDevicePin(device.id, pinObj)
    pinList.append(pin)
  return {
    device: device,
    pinList: pinList
  }

def pluginDevicePin(pinId, boardID):
  updatedPin = dao.updateDevicePinBoardId(pinId, boardID)
  return updatedPin

def unplugDevicePin(pinId):
  updatedPin = dao.updateDevicePinBoardId(pinId, -1)
  return updatedPin