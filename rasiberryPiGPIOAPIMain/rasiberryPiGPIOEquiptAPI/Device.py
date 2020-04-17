class Device:
  def __init__(self, deviceName, pinListRequired, interfaceType): #pinList:[ {pinFunction: 0, pinMode: 0} ]
    self.deviceName = deviceName
    self.pinList = pinListRequired
    self.interfaceType = interfaceType
  
  def getDeviceName(self):
    return self.deviceName
  
  def getPinList(self):
    return self.pinList

  def getInterfaceType(self):
    return self.interfaceType