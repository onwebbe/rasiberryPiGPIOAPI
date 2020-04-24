from django.db import models
import django.utils.timezone as timezone

class Scheduler(models.Model):
  scheduleName = models.CharField(max_length=32)
  scheduleType = models.IntegerField(default=1) #1 every
  scheduleMode = models.IntegerField(default=1) #1 every second 2 every min 3 every hour 4 every day
  scheduleValue = models.IntegerField(default=1) # for exmple every 3 second, input 3 here and 1 in scheduleMode
  otherSchedule = models.CharField(max_length=64)
  scheduleJobName = models.CharField(max_length=32)
  scheduleStatus = models.IntegerField(default=2) #1 running 2 stopped
  active = models.IntegerField(default=1) #1 active 2 deActive
  piDeviceID = models.IntegerField(default=-1)
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '定时器'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.scheduleName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['scheduleName'] = self.scheduleName
    obj['scheduleType'] = self.scheduleType
    obj['scheduleMode'] = self.scheduleMode
    obj['scheduleValue'] = self.scheduleValue
    obj['otherSchedule'] = self.otherSchedule
    obj['scheduleJobName'] = self.scheduleJobName
    obj['scheduleStatus'] = self.scheduleStatus
    obj['piDeviceId'] = self.piDeviceID
    return obj