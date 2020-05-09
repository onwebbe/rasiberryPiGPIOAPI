from rasiberryPiGPIOEquiptAPI.models import DeviceInfo
from rasiberryPiGPIOEquiptAPI.models import DevicePin
from rasiberryPiGPIOEquiptAPI.models import PiDeviceInfo
from rasiberryPiGPIOEquiptAPI.models import PiDevicePin
from rasiberryPiGPIOEquiptAPI.models import DeviceData
from rasiberryPiGPIOEquiptAPI.models import DeviceDataHistory

def getHistoryDeviceData(piDeviceId, deviceDataName, dateFrom, dateTo):
  return DeviceDataHistory.objects.filter(dataDateTime__gte=dateFrom, dataDateTime__lt=dateTo, piDeviceID = piDeviceId, deviceDataName__in = deviceDataName)

def getHistoryDeviceAllData(piDeviceId, dateFrom, dateTo):
  return DeviceDataHistory.objects.filter(dataDateTime__gte=dateFrom, dataDateTime__lt=dateTo, piDeviceID = piDeviceId)