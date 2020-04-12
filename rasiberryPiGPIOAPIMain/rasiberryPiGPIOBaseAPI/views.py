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
    pinStatus = pin.read()
    pinBCM = pin.getBCM()
    pinBoard = pin.getBOARD()
    pinName = pin.getName()
    pinData = {}
    pinData['pinStatus'] = pinStatus
    pinData['BCM'] = pinBCM
    pinData['Physical'] = pinBoard
    pinData['Name'] = pinName
    pinListData.append(pinData)
  
  piData = {}
  piData["mode"] = mode
  piData["type"] = piType
  piData["pinList"] = pinListData
  return ResponseProcessor.processSuccessResponse(piData)

def gpio_setPinStatus():
  pass

def gpio_getPinStatus():
  pass

def gpio_pwn_start():
  pass

def gpio_pwn_change_duty_cycle():
  pass

def gpio_pwn_stop():
  pass