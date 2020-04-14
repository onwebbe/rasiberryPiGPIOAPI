from .MyEncoder import MyEncoder
from django.http import HttpResponse
from django.shortcuts import render
import json

def processSuccessResponse(obj = ''):
  responseObj = {}
  responseObj["success"] = True
  responseObj["data"] = obj
  return HttpResponse(json.dumps(responseObj, cls=MyEncoder, indent=2))


def processFailResponse(msg):
  responseObj = {}
  responseObj["success"] = False
  responseObj["msg"] = msg
  return HttpResponse(json.dumps(responseObj, cls=MyEncoder, indent=2))