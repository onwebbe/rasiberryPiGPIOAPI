from django.shortcuts import render
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin

import rasiberryPiGPIOBaseController.equiptments.SimpleEquipt as SimpleEquipt

import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor

import rasiberryPiGPIOAPIMain.PiGPIO as PiGPIO

from django.http import HttpResponse
from django.shortcuts import render
import json

pi = PiGPIO.PI

def led(request, boardID, switch):
  pinObj = pi.getPinByBoardId(boardID)
  LED = SimpleEquipt.LED(pinObj)
  if (switch == 'ON'):
    LED.light()
  else:
    LED.shutdown()

  pinStatus = ''
  pinBCM = pinObj.getBCM()
  pinBoard = pinObj.getBOARD()
  pinName = pinObj.getName()
  pinMode = pinObj.getMode()
  if (pinMode == 'IN'):
    pinStatus = pinObj.read()
  elif (pinMode == 'OUT'):
    pinStatus = pinObj.getValue()
  else:
    pinStatus = ''
  pinData = {}
  pinData['pinStatus'] = pinStatus
  pinData['BCM'] = pinBCM
  pinData['Physical'] = pinBoard
  pinData['Name'] = pinName
  pinData['mode'] = pinMode
  return ResponseProcessor.processSuccessResponse({'pin':pinData, 'switch': switch})
