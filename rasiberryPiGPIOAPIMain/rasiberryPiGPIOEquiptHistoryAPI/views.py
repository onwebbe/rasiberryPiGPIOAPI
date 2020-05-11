from django.shortcuts import render
import rasiberryPiGPIOEquiptHistoryAPI.HistoryDao as historyDao
import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor
from datetime import datetime
from datetime import date
# Create your views here.
def _getHistoryData(piDeviceId, dateFromObj, dateToObj, deviceDataNames):
  
  if (deviceDataNames is not None):
    deviceDataNameList = []
    deviceDataNameList = deviceDataNames.split(',')
    historyDataList = historyDao.getHistoryDeviceData(piDeviceId, deviceDataNameList, dateFromObj, dateToObj)
  else:
    historyDataList = historyDao.getHistoryDeviceAllData(piDeviceId, dateFromObj, dateToObj)
  historyDataObjList = []
  for historyData in historyDataList:
    historyDataObjList.append(historyData._convertToDict())
  return historyDataObjList

def getHistoryData(request, piDeviceId):
  dateFrom = request.GET.get('from')
  dateTo = request.GET.get('to')
  dateFromObj = None
  dateToObj = None
  if (dateFrom is None):
     dateFromObj = datetime.now()
  else:
    dateFromObj = datetime.strptime(dateFrom, '%Y-%m-%d %H:%M:%S')
  if (dateTo is None):
     dateToObj = datetime.now()
  else:
    dateToObj = datetime.strptime(dateTo, '%Y-%m-%d %H:%M:%S')
  deviceDataNames = request.GET.get('names')
  historyDataObjList = _getHistoryData(piDeviceId, dateFromObj, dateToObj, deviceDataNames)
  return ResponseProcessor.processSuccessResponse(historyDataObjList)

def getTodaySingleGraphData(request, piDeviceId, deviceDataName):
  category = []
  data = []
  dateFrom = date.today()
  dateTo = date.today()
  dateTo = dateTo.replace(day = dateTo.day + 1)
  print(dateFrom)
  print(dateTo)
  # dateFrom = datetime.strptime('2020-04-27 00:00:00', '%Y-%m-%d %H:%M:%S')
  # dateTo = datetime.strptime('2020-04-28 00:00:00', '%Y-%m-%d %H:%M:%S')
  

  listData = _getHistoryData(piDeviceId, dateFrom, dateTo, deviceDataName)
  for listitem in listData:
    data.append(listitem['deviceDataValue'])
    timeObj = listitem['dataDateTime']
    displayTime = timeObj.strftime('%H:%M')
    category.append(displayTime)
  
  result = {}
  result['category'] = category
  result['data'] = data
  return ResponseProcessor.processSuccessResponse(result)
