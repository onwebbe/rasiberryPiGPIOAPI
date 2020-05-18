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

def getAllDeviceHistoryChart():
  return DeviceDataHistoryChart.objects.all()

def addNewDeviceHistoryChart(piDeviceId, deviceDataName, title, unit, displayType):
  chart = DeviceDataHistoryChart(piDeviceID = piDeviceId, deviceDataName = deviceDataName, title = title, displayType = displayType, unit = unit)
  chart.save()
  return chart

def updateDeviceHistoryChart(chartId, piDeviceId, deviceDataName, title, unit, displayType):
  chart = DeviceDataHistoryChart.objects.get(id = chartId)
  if (piDeviceId is None):
    piDeviceId = chart.piDeviceID
  if (deviceDataName is None):
    deviceDataName = chart.deviceDataName
  if (title is None):
    title = chart.title
  if (unit is None):
    unit = chart.unit
  if (displayType is None):
    displayType = chart.displayType
  DeviceDataHistoryChart.objects.filter(id = chartId).update(piDeviceID = piDeviceId, deviceDataName = deviceDataName, title = title, displayType = displayType, unit = unit)
  return DeviceDataHistoryChart.objects.get(id = chartId)

def deleteDeviceHistoryChart(chartId):
  DeviceDataHistoryChart.objects.filter(id = chartId).delete()
  pass

def getDeviceDataNamesByDeviceId(piDeviceId):
  return DeviceDataHistory.objects.filter(piDeviceID = piDeviceId).values('deviceDataName').order_by('deviceDataName').distinct()