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

import rasiberryPiGPIOEquiptAPI.DAO as dao
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import INTERFACE as INTERFACE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import STATUS as STATUS
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_FUCNTION as PIN_FUCNTION
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import PIN_MODE as PIN_MODE
from rasiberryPiGPIOEquiptAPI.InterfaceConstans import getDictKeyByName as getDictKeyByName

from wsgiref.util import FileWrapper
import os
import mimetypes
pi = PiGPIO.PI


def init(request):
  InitialDatabaseSetup.run()
  return ResponseProcessor.processSuccessResponse()

def getDevices(request):
  deviceList = dao.getDevices()
  deviceObjList = []
  for device in deviceList:
    deviceObj = device._convertToDict()
    deviceObj['deviceInterfaceType_TR'] = getDictKeyByName(INTERFACE, deviceObj['deviceInterfaceType'])
    deviceObjList.append(deviceObj)
  return ResponseProcessor.processSuccessResponse(deviceObjList)

def createPiDevice(request, deviceId):
  name = request.GET.get('name')
  if (name is not None):
    piDevice = dao.addPiDevice(deviceId, name)
    piDeviceObj = piDevice._convertToDict()
    devicePinList = dao.getDevicePinByDeviceId(deviceId)
    devicePinObjList = []
    for devicePin in devicePinList:
      devicePinID = devicePin.id
      piDevicePinObj = dao.addPiDevicePin(piDevice.id, [{'pinBoardId': -1, 'devicePinID': devicePinID, 'value': None}])
      piDevicePinObj = piDevicePinObj[0]
      piDevicePinObj = piDevicePinObj._convertToDict()
      devicePinObjList.append(piDevicePinObj)
    piDeviceObj['pinList'] = devicePinObjList
    return ResponseProcessor.processSuccessResponse(piDeviceObj)
  else:
    return ResponseProcessor.processFailResponse("设备名字为空")

def updatePiDevice(request, piDeviceId):
  name = request.GET.get('name')
  updatedPiDevice = dao.updatePiDevice(piDeviceId, name)
  return ResponseProcessor.processSuccessResponse(updatedPiDevice._convertToDict())

def deletePiDeviceById(request, piDeviceId):
  dao.deletePiDevice(piDeviceId)
  return ResponseProcessor.processSuccessResponse()

def getPiDevices(request):
  deviceList = dao.getPiDevices()
  deviceObjList = []
  for device in deviceList:
    deviceObj = device._convertToDict()
    deviceObj['status_TR'] = getDictKeyByName(STATUS, deviceObj['status'])
    piDevicePinList = _getPiDevicePin(device.id)
    deviceObj['pinList'] = piDevicePinList
    deviceObjList.append(deviceObj)
  return ResponseProcessor.processSuccessResponse(deviceObjList)

def getPiDeviceById(request, piDeviceId):
  piDevice = dao.getPiDeviceById(piDeviceId)
  return ResponseProcessor.processSuccessResponse(piDevice._convertToDict())

def getPiDevicesByDeviceId(request, deviceId):
  piDeviceList = dao.getPiDeviceByDeviceId(deviceId)
  piDeviceObjList = []
  for piDevice in piDeviceList:
    piDeviceObj = piDevice._convertToDict()
    piDeviceObjList.append(piDeviceObj)
  return ResponseProcessor.processSuccessResponse(piDeviceObjList)

def _getPiDevicePin(piDeviceId):
  devicePinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  devicePinObjList = []
  for pidevicepind in devicePinList:
    deviceObj = pidevicepind._convertToDict()
    devicePin = _getPiDevicePinDetail(deviceObj['devicePinID'])
    deviceObj['devicePinDetail'] = devicePin
    devicePinObjList.append(deviceObj)
  return devicePinObjList

def getPiDevicePin(request, piDeviceId):
  devicePinObjList = _getPiDevicePin(piDeviceId)
  return ResponseProcessor.processSuccessResponse(devicePinObjList)

def _getPiDevicePinDetail(devicePinId):
  devicePin = dao.getDevicePinById(devicePinId)
  if (devicePin is not None):
    devicePinObj = devicePin._convertToDict()
    devicePinObj['pinMode_TR'] = getDictKeyByName(PIN_MODE, devicePinObj['pinMode'])
    devicePinObj['pinFunction_TR'] = getDictKeyByName(PIN_FUCNTION, devicePinObj['pinFunction'])
    return devicePinObj
  else:
    return {}

def attachPiDevicePinToBoard(request, piDevicePinId):
  boardID = request.GET.get('boardId')
  updatedPiDevicePin = dao.updateDevicePinBoardId(piDevicePinId, boardID)
  updatedPiDevicePin = dao.getPiDevicePinById(piDevicePinId)
  return ResponseProcessor.processSuccessResponse(updatedPiDevicePin._convertToDict())

def unAttachPiDevicePinToBoard(request, piDevicePinId):
  updatedPiDevicePin = dao.updateDevicePinBoardId(piDevicePinId, -1)
  updatedPiDevicePin = dao.getPiDevicePinById(piDevicePinId)
  return ResponseProcessor.processSuccessResponse(updatedPiDevicePin._convertToDict())

def start(request):
  pass

def led(request, piDeviceId, switch):
  pinList = dao.getPiDevicePinByPiDeviceId(piDeviceId)
  boardID = None
  for pin in pinList:
    piDevicePinObj = pin._convertToDict()
    devicePinObj = _getPiDevicePinDetail(piDevicePinObj['devicePinID'])
    if (devicePinObj['pinFunction'] == PIN_FUCNTION['GPIO']):
      boardID = pin.pinBoardID
  if (boardID is not None):
    led = SimpleEquipt.LED(pi.getPinByBoardId(boardID))
    if (switch == 'on'):
      led.light()
    else:
      led.shutdown()
  return ResponseProcessor.processSuccessResponse()

def getDeviceImage(request, deviceId):
  image_path = request.GET.get('path')
  print(image_path)
  fileWrapper = FileWrapper(open(image_path, 'rb'))
  content_type = mimetypes.guess_type(image_path)[0]
  contentLength = os.path.getsize(image_path)
  response = HttpResponse(fileWrapper, content_type = content_type)
  response['Content-Length']      = contentLength
  response['Content-Disposition'] = "attachment; filename=%s" %  image_path
  return response
