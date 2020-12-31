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
from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import HSensorRotation as HSensorRotation
from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import HSensorRotationV2 as HSensorRotationV2

from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import Motor as Motor

from rasiberryPiGPIOEquiptAPI.views import pi

from wsgiref.util import FileWrapper
import os
import mimetypes
pi = PiGPIO.PI

motors = []
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
    bmpDataObj['pressure'] = round( pressure / 100, 0 ) 
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
    gy30DataObj['lx'] = round(lightData, 0)
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
      boardPinID = pin.pinBoardID
      boardPinObject = pi.getPinByBoardId(boardPinID)
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

def _getRotationCountData(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  deviceData = -1
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    boardID = pin.pinBoardID
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      rotationSensor = HSensorRotation.getInstance(pi.getPinByBoardId(boardID))
      deviceData = rotationSensor.getLastCountResult()
      break
  return deviceData

def getRotationCountData(request, piDeviceId):
  deviceData = _getRotationCountData(piDeviceId)
  return ResponseProcessor.processSuccessResponse(deviceData)

def startMotor(request, piDeviceId, direction, speed):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  gpioList = []
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    boardID = pin.pinBoardID
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      gpioList.append(pi.getPinByBoardId(boardID))
  motor = Motor(gpioList[0], gpioList[1])
  motor.start(direction, speed)
  motorCacheData = {}
  motorCacheData['piDeviceId'] = piDeviceId
  motorCacheData['motorObj'] = motor
  return ResponseProcessor.processSuccessResponse()

def _getRotationCountDataV2(piDeviceId):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  deviceData = -1
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    boardID = pin.pinBoardID
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      rotationSensor = HSensorRotationV2.getInstance(pi.getPinByBoardId(boardID))
      deviceData = rotationSensor.getAvgData(5)
      break
  return deviceData

def getRotationCountDataV2(request, piDeviceId):
  deviceData = _getRotationCountDataV2(piDeviceId)
  return ResponseProcessor.processSuccessResponse(deviceData)