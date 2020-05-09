from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class DeviceInfo(models.Model):
  deviceName = models.CharField(max_length=32)
  deviceType = models.CharField(max_length=32)
  deviceInCategory = models.CharField(max_length=64, default='')
  i2cAddress = models.IntegerField(default=None)
  deviceInterfaceType = models.IntegerField(default=0)  #0 GPIO 1 PWM 2 I2C defined in InterfaceConstans.py
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.deviceName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['deviceName'] = self.deviceName
    obj['deviceType'] = self.deviceType
    obj['deviceInCategory'] = self.deviceInCategory
    obj['deviceInterfaceType'] = self.deviceInterfaceType
    obj['i2cAddress'] = self.i2cAddress
    return obj

class DevicePin(models.Model):
  deviceID = models.IntegerField()
  pinMode = models.IntegerField() # -1 None 0 IN   1 OUT
  pinFunction = models.IntegerField() #'GND': 0, 'GPIO': 1, '3V': 2, '5V': 3, 'SDA': 4, 'SDL': 5 defined in InterfaceConstans.py
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备所需pin口'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.pinFunction
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['deviceID'] = self.deviceID
    obj['pinMode'] = self.pinMode
    obj['pinFunction'] = self.pinFunction
    return obj

# Create your models here.
class PiDeviceInfo(models.Model):
  piDeviceName = models.CharField(max_length=32)
  deviceID = models.IntegerField()
  status = models.IntegerField(default=0) #0 unbind #1 bind
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.deviceName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['piDeviceName'] = self.piDeviceName
    obj['deviceID'] = self.deviceID
    obj['status'] = self.status
    return obj

class PiDevicePin(models.Model):
  piDeviceID = models.IntegerField()
  pinBoardID = models.IntegerField()
  devicePinID = models.IntegerField()
  pinValue = models.CharField(max_length=32)
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备所需pin口'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.pinBoardID + self.pinValue
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['piDeviceID'] = self.piDeviceID
    obj['pinBoardID'] = self.pinBoardID
    obj['devicePinID'] = self.devicePinID
    obj['pinValue'] = self.pinValue
    return obj

class DeviceData(models.Model):
  piDeviceID = models.IntegerField()
  deviceDataName = models.CharField(max_length=32)
  deviceDataValue = models.CharField(max_length=32)
  deviceUpdatedDataTime = models.DateTimeField('device data time', default = timezone.now)
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备采集的数据'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.piDeviceID + self.deviceDataName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['piDeviceID'] = self.piDeviceID
    obj['deviceDataName'] = self.deviceDataName
    obj['deviceDataValue'] = self.deviceDataValue
    obj['deviceUpdatedDataTime'] = self.deviceUpdatedDataTime.isoformat()
    return obj

class DeviceDataHistory(models.Model):
  piDeviceID = models.IntegerField()
  deviceDataName = models.CharField(max_length=32)
  deviceDataValue = models.CharField(max_length=32)
  dataDateTime = models.DateTimeField('device data time', default = timezone.now)
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备数据的历史记录'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.piDeviceID + self.deviceDataName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['piDeviceID'] = self.piDeviceID
    obj['deviceDataName'] = self.deviceDataName
    obj['deviceDataValue'] = self.deviceDataValue
    obj['dataDateTime'] = self.dataDateTime
    return obj