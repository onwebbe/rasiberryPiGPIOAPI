from django.shortcuts import render
import rasiberryPiGPIOEquiptHistoryAPI.HistoryDao as historyDao
import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor
from datetime import datetime
from datetime import date
import django.utils.timezone as timezone
import pytz
import json
from rasiberryPiGPIOEquiptHistoryAPI.models import DeviceDataHistoryChart
from django.views.decorators.http import require_GET, require_http_methods, require_POST

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
     dateFromObj = timezone.now()
  else:
    dateFromObj = datetime.strptime(dateFrom, '%Y-%m-%d %H:%M:%S')
  if (dateTo is None):
     dateToObj = timezone.now()
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
    timeObj = timeObj.astimezone(pytz.timezone('Asia/Shanghai'))
    displayTime = timeObj.strftime('%H:%M')
    category.append(displayTime)
  
  result = {}
  result['category'] = category
  result['data'] = data
  return ResponseProcessor.processSuccessResponse(result)

@require_GET
def getHistoryChartList(request):
  chartList = historyDao.getAllDeviceHistoryChart()
  chartObjList = []
  for chart in chartList:
    chartObjList.append(chart._convertToDict())
  return ResponseProcessor.processSuccessResponse(chartObjList)

@require_POST
def addHistoryChart(request):
  postBody = request.body
  postData = json.loads(postBody)
  piDeviceId = postData['piDeviceID']
  deviceDataName = postData['deviceDataName']
  title = postData['title']
  unit = postData['unit']
  displayType = postData['displayType']
  resultChart = historyDao.addNewDeviceHistoryChart(piDeviceId, deviceDataName, title, unit, displayType)
  return ResponseProcessor.processSuccessResponse(resultChart._convertToDict())

@require_POST
def updateHistoryChart(request, chartId):
  postBody = request.body
  postData = json.loads(postBody)
  piDeviceId = None if ('piDeviceID' not in postData) else postData['piDeviceID']
  deviceDataName = None if ('deviceDataName' not in postData) else postData['deviceDataName']
  title = None if ('title' not in postData) else postData['title']
  unit =  None if ('unit' not in postData) else postData['unit']
  displayType = None if ('displayType' not in postData) else postData['displayType']
  resultChart = historyDao.updateDeviceHistoryChart(chartId, piDeviceId, deviceDataName, title, unit, displayType)
  return ResponseProcessor.processSuccessResponse(resultChart._convertToDict())

@require_GET
def deleteHistoryChart(request, chartId):
  historyDao.deleteDeviceHistoryChart(chartId)
  return ResponseProcessor.processSuccessResponse()

@require_GET
def getDeviceDataNamesByDeviceId(request, piDeviceId):
  dataNames = historyDao.getDeviceDataNamesByDeviceId(piDeviceId)
  dataNameStrs = []
  for dataName in dataNames:
    dataNameStrs.append(dataName['deviceDataName'])
  return ResponseProcessor.processSuccessResponse(dataNameStrs)