from django.shortcuts import render
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin

import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor

import rasiberryPiGPIOAPIMain.PiGPIO as PiGPIO

from . import Constants
from django.http import HttpResponse
from django.shortcuts import render
import json
import schedule

from . import DAO as dao

import rasiberryPiGPIOEquiptAPI.DAO as eqDao


import rasiberryPiGPIOEquiptAPI.DevicesView as DevicesView
pi = PiGPIO.PI
# Create your views here.
def gpio_overview(request):
  mode = pi.getMode()
  piType = pi.getType()
  pinList = pi.pins

  pinListData = []
  for pin in pinList:
    pinStatus = ''
    pinBCM = pin.getBCM()
    pinBoard = pin.getBOARD()
    pinName = pin.getName()
    pinMode = pin.getMode()
    if (pinMode == 'IN'):
      pinStatus = pin.read()
    elif (pinMode == 'OUT'):
      pinStatus = pin.getValue()
    else:
      pinStatus = ''
    pinData = {}
    pinData['pinStatus'] = pinStatus
    pinData['BCM'] = pinBCM
    pinData['Physical'] = pinBoard
    pinData['Name'] = pinName
    pinData['mode'] = pinMode
    pinListData.append(pinData)
  
  piData = {}
  piData["mode"] = mode
  piData["type"] = piType
  piData["pinList"] = pinListData
  return ResponseProcessor.processSuccessResponse(piData)

def gpio_setPinStatus(request, boardID, level):
  pin = pi.getPinByBoardId(boardID)
  setupLevel = None
  if (level == 1):
    setupLevel = Pin.PIN_HIGH
  else:
    setupLevel = Pin.PIN_LOW
  if (pin is not None):
    pin.output_setup(setupLevel)
  return ResponseProcessor.processSuccessResponse({'boardId': boardID, 'level':setupLevel})

def gpio_getPinStatus(request, boardID):
  data = None
  pin = pi.getPinByBoardId(boardID)
  if (pin is not None):
    data = pin.read()
  return ResponseProcessor.processSuccessResponse(data)

def gpio_pwn_start(request, boardID):
  pin = pi.getPinByBoardId(boardID)
  if (pin is not None):
    pin.PWM_setup()
  return ResponseProcessor.processSuccessResponse()

def gpio_pwn_change_duty_cycle(request, boardID, cycle):
  pin = pi.getPinByBoardId(boardID)
  if (pin is not None):
    pin.PWM_ChangeDutyCycle(cycle)
  return ResponseProcessor.processSuccessResponse()

def gpio_pwn_change_frequency(request, boardID, frequency):
  pin = pi.getPinByBoardId(boardID)
  if (pin is not None):
    pin.PWM_ChangeFrequency(frequency)
  return ResponseProcessor.processSuccessResponse()

def gpio_pwn_stop(request, boardID):
  pin = pi.getPinByBoardId(boardID)
  if (pin is not None):
    pin.PWM_stop()
  return ResponseProcessor.processSuccessResponse()

def create_scheduler(request):
  scheduleName = request.GET.get('scheduleName')
  scheduleMode = Constants.SCHEDULE_MODE[request.GET.get('scheduleMode')]
  scheduleValue = int(request.GET.get('scheduleValue'))
  scheduleJobName = request.GET.get('scheduleJobName')
  createdScheduler = dao.createScheduler(scheduleName, scheduleMode, scheduleValue, scheduleJobName)
  return ResponseProcessor.processSuccessResponse(createdScheduler._convertToDict())

def start_scheduler(request, schedulerId):
  scheduler = dao.startAScheduler(schedulerId)
  return ResponseProcessor.processSuccessResponse(scheduler._convertToDict())

def stop_scheduler(request, schedulerId):
  scheduler = dao.stopAScheduler(schedulerId)
  return ResponseProcessor.processSuccessResponse(scheduler._convertToDict())

def start_process_scheduler(request):
  activeScheduleList = dao.findAllActiveScheduler()
  scheduledJobs = []
  for scheduler in activeScheduleList:
    schedulerObj = scheduler._convertToDict()
    schedulerId = schedulerObj['id']
    jobName = schedulerObj['scheduleJobName']
    piDeviceId = schedulerObj['piDeviceID']
    scheduleMode = schedulerObj['scheduleMode']
    scheduleValue = schedulerObj['scheduleValue']
    if (scheduleMode == Constants.SCHEDULE_MODE['SECONDS']):
      schedule.every(scheduleValue).seconds.do(saveJob, request, piDeviceId)
    elif (scheduleMode == Constants.SCHEDULE_MODE['MINUTS']):
      schedule.every(scheduleValue).minutes.do(saveJob, request, piDeviceId)
    elif (scheduleMode == Constants.SCHEDULE_MODE['HOUR']):
      schedule.every(scheduleValue).hour.do(saveJob, request, piDeviceId)
    elif (scheduleMode == Constants.SCHEDULE_MODE['DAY']):
      schedule.every(scheduleValue).day.do(saveJob, request, piDeviceId)
    scheduledJobs.append(dao.startAScheduler(schedulerId)._convertToDict())
  return ResponseProcessor.processSuccessResponse(scheduledJobs)

def saveJob(request, piDeviceId):
  data = _saveJob(piDeviceId)
  return ResponseProcessor.processSuccessResponse(data)
  
def _saveJob(piDeviceId):
  savedDataList = []
  piDevice = eqDao.getPiDeviceById(piDeviceId)
  deviceId = piDevice.deviceID
  device = eqDao.getDeviceById(deviceId)
  jobName = device.deviceType
  if (jobName == 'DHT22'):
    data = DevicesView._getDHT22Data(piDeviceId)
    # data = {
    #   'temperature': 10,
    #   'humidity': 40
    # }
    d1 = eqDao.saveDeviceData(piDeviceId, 'temperature', data['temperature'])
    d2 = eqDao.saveDeviceData(piDeviceId, 'humidity', data['humidity'])
    savedDataList.append(d1._convertToDict())
    savedDataList.append(d2._convertToDict())
  elif (jobName == 'BMP180'):
    data = DevicesView._getBMP180Data(piDeviceId)
    d1 = eqDao.saveDeviceData(piDeviceId, 'temperature', data['temperature'])
    d2 = eqDao.saveDeviceData(piDeviceId, 'pressure', data['pressure'])
    d3 = eqDao.saveDeviceData(piDeviceId, 'altitude', data['altitude'])
    savedDataList.append(d1._convertToDict())
    savedDataList.append(d2._convertToDict())
    savedDataList.append(d3._convertToDict())
  elif (jobName == 'GY30'):
    data = DevicesView._getGY30Data(piDeviceId)
    d1 = eqDao.saveDeviceData(piDeviceId, 'lx', data['lx'])
    savedDataList.append(d1._convertToDict())
  return savedDataList