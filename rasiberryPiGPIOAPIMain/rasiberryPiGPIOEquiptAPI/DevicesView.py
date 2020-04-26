from django.shortcuts import render
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin

import rasiberryPiGPIOBaseController.equiptments.SimpleEquipt as SimpleEquipt

import rasiberryPiGPIOAPIMain.ResponseProcessor as ResponseProcessor

import rasiberryPiGPIOAPIMain.PiGPIO as PiGPIO

from django.http import HttpResponse
from django.shortcuts import render
import json

import rasiberryPiGPIOEquiptAPI.service.InitialDatabaseSetup as InitialDatabaseSetup
from rasiberryPiGPIOEquiptAPI.views import _getPiDevicePinDetail as _getPiDevicePinDetail
import rasiberryPiGPIOEquiptAPI.DAO as dao
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import INTERFACE as INTERFACE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import STATUS as STATUS
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_FUCNTION as PIN_FUCNTION
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_MODE as PIN_MODE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import getDictKeyByName as getDictKeyByName
from rasiberryPiGPIOBaseController.equiptments.Temperature import DHT22 as DHT22
from rasiberryPiGPIOBaseController.equiptments.Pressure import BMP180 as BMP180
from rasiberryPiGPIOBaseController.equiptments.LightSensor import GY30 as GY30

from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import RainDrop as RainDrop

from wsgiref.util import FileWrapper
import os
import mimetypes
pi = PiGPIO.PI

def _getDHT22Data(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  boardID = None
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      boardID = pin.pinBoardID
  dhtDataObj = {
    'temperature': None,
    'humidity': None
  }
  if (boardID is not None):
    dht22 = DHT22(pi.getPinByBoardId(boardID))
    dhtData = dht22.getData()
    temperature = dhtData[0]
    humidity = dhtData[1]
    dhtDataObj['temperature'] = temperature
    dhtDataObj['humidity'] = humidity
  return dhtDataObj

def getDHT22Data(request, piDeviceId):
  dhtDataObj = _getDHT22Data(piDeviceId)
  return ResponseProcessor.processSuccessResponse(dhtDataObj)

def _getBMP180Data(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  SDAPin = None
  SDLPin = None
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['SDA']):
      SDAPin = pin.pinBoardID
    elif (devicePinObj['pinFunction'] == PIN_FUCNTION['SDL']):
      SDLPin = pin.pinBoardID
  bmpDataObj = {
    'temperature': None,
    'pressure': None, 
    'altitude': None
  }
  if (SDAPin is not None and SDLPin is not None):
    bmp180 = BMP180()
    pressure = bmp180.getPressure()
    altitude = bmp180.getAltitude() + 95
    temperature = bmp180.getTemperature()
    bmpDataObj['temperature'] = temperature
    bmpDataObj['pressure'] = round( pressure, 0 ) / 100
    bmpDataObj['altitude'] = round( altitude, 0 )
  return bmpDataObj

def getBMP180Data(request, piDeviceId):
  bmpDataObj = _getBMP180Data(piDeviceId)
  return ResponseProcessor.processSuccessResponse(bmpDataObj)

def _getGY30Data(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  SDAPin = None
  SCLPin = None
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['SDA']):
      SDAPin = pin.pinBoardID
    elif (devicePinObj['pinFunction'] == PIN_FUCNTION['SDL']):
      SCLPin = pin.pinBoardID
  gy30DataObj = {
    'lx': None
  }
  if (SDAPin is not None and SCLPin is not None):
    gy30 = GY30()
    lightData = gy30.getLightData()
    gy30DataObj['lx'] = round(lightData, 2)
  return gy30DataObj

def getGY30Data(request, piDeviceId):
  gy30DataObj = _getGY30Data(piDeviceId)
  return ResponseProcessor.processSuccessResponse(gy30DataObj)

def _getRainDropData(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  boardPinObject = None
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      boardPinObject = pin
  dropDataObj = {
    'rain': 'no rain'
  }
  if (boardPinObject is not None):
    rainDropDevice = RainDrop(boardPinObject)
    if (rainDropDevice.isDrop()):
      dropDataObj['rain'] = 'rain'
    
  return dropDataObj

def getRainDropData(request, piDeviceId):
  dropDataObj = _getRainDropData(piDeviceId)
  return ResponseProcessor.processSuccessResponse(dropDataObj)