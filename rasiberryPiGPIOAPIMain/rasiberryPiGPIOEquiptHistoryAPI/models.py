from django.db import models

# Create your models here.
class DeviceDataHistoryChart(models.Model):
  piDeviceID = models.IntegerField()
  deviceDataName = models.CharField(max_length=32)
  title = models.CharField(max_length=36)
  active = models.SmallIntegerField(default = 0)  # 0: active 1: inactive
  class Meta:
    #db_table = 'tb_books'  # 指明数据库表名
    verbose_name = '设备数据图表'  # 在admin站点中显示的名称
    verbose_name_plural = verbose_name  # 显示的复数名称

  def __str__(self):
    """定义每个数据对象的显示信息"""
    return self.title + ':' + self.piDeviceID + ':' + self.deviceDataName
  
  def _convertToDict(self):
    obj = {}
    obj['id'] = self.id
    obj['piDeviceID'] = self.piDeviceID
    obj['deviceDataName'] = self.deviceDataName
    obj['title'] = self.title
    obj['active'] = self.active
    return obj