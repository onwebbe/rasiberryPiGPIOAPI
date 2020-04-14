from django.shortcuts import render
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin

import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor

from django.http import HttpResponse
from django.shortcuts import render
import json

pi = RasiberryPiGPIO.RasiberryPiGPIO("3B+", "BCM")
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
    if (pinMode == 'IN' or pinMode == 'OUT'):
      pinStatus = pin.read()
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