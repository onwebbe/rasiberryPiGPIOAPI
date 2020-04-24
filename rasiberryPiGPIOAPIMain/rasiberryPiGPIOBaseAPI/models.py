from django.db import models
import django.utils.timezone as timezone

class Scheduler(models.Model):
  scheduleName = models.CharField(max_length=32)
  scheduleType = models.IntegerField(default=1) #1 every
  scheduleMode = models.IntegerField(default=1) #1 every second 2 every min 3 every hour 4 every day
  scheduleValue = models.IntegerField(default=1) # for exmple every 3 second, input 3 here and 1 in scheduleMode
  otherSchedule = models.CharField(max_length=64)
  scheduleJobName = models.CharField(max_length=32)
  scheduleStatus = models.IntegerField(default=1) #1 running 2 stopped
