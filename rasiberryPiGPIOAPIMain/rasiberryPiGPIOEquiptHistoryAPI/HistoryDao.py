from rasiberryPiGPIOEquiptAPI.models import DeviceInfo
from rasiberryPiGPIOEquiptAPI.models import DevicePin
from rasiberryPiGPIOEquiptAPI.models import PiDeviceInfo
from rasiberryPiGPIOEquiptAPI.models import PiDevicePin
from rasiberryPiGPIOEquiptAPI.models import DeviceData
from rasiberryPiGPIOEquiptAPI.models import DeviceDataHistory
from rasiberryPiGPIOEquiptHistoryAPI.models import DeviceDataHistoryChart

def getHistoryDeviceData(piDeviceId, deviceDataName, dateFrom, dateTo):
  return DeviceDataHistory.objects.filter(dataDateTime__gte=dateFrom, dataDateTime__lt=dateTo, piDeviceID = piDeviceId, deviceDataName__in = deviceDataName)

def getHistoryDeviceAllData(piDeviceId, dateFrom, dateTo):
  return DeviceDataHistory.objects.filter(dataDateTime__gte=dateFrom, dataDateTime__lt=dateTo, piDeviceID = piDeviceId)

def addNewDeviceHistoryChart(piDeviceId, deviceDataName, title):
  chart = DeviceDataHistoryChart(piDeviceID = piDeviceId, deviceDataName = deviceDataName, title = title)
  chart.save()
  return chart

def updateDeviceHistoryChart(chartId, piDeviceId, deviceDataName, title):
  DeviceDataHistoryChart.objects.filter(id = chartId).update(piDeviceID = piDeviceId, deviceDataName = deviceDataName, title = title)
  return DeviceDataHistoryChart.objects.get(id = chartId)._convertToDict()

def deleteDeviceHistoryChart(chartId):
  DeviceDataHistoryChart.objects.filter(id = chartId).delete()
  pass