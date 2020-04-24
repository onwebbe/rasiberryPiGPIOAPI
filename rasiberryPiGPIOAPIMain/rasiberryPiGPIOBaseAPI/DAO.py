from . import models
from . import Constants

def createScheduler(scheduleName, scheduleMode, scheduleValue, scheduleJobName):
  scheduler = models.Scheduler(scheduleName = scheduleName, scheduleMode = scheduleMode, scheduleValue = scheduleValue, scheduleJobName = scheduleJobName, scheduleType = 1)
  scheduler.save()
  return scheduler

def getSchedulers():
  return models.Scheduler.objects.all()

def getSchedulerById(schedulerId):
  return models.Scheduler.objects.get(id = schedulerId)
  
def startAScheduler(schedulerId):
  models.Scheduler.objects.filter(id = schedulerId).update(scheduleStatus = Constants.SCHEDULE_STATUS['RUNNING'])
  return getSchedulerById(schedulerId)

def stopAScheduler(schedulerId):
  models.Scheduler.objects.filter(id = schedulerId).update(scheduleStatus = Constants.SCHEDULE_STATUS['STOPPED'])
  return getSchedulerById(schedulerId)

def activeAScheduler(schedulerId):
  models.Scheduler.objects.filter(id = schedulerId).update(active = Constants.SCHEDULE_ACTIVE['ACTIVE'])
  return getSchedulerById(schedulerId)

def deActiveAScheduler(schedulerId):
  models.Scheduler.objects.filter(id = schedulerId).update(active = Constants.SCHEDULE_ACTIVE['DEACTIVE'])
  return getSchedulerById(schedulerId)

def findAllActiveScheduler():
  return models.Scheduler.objects.filter(active = Constants.SCHEDULE_ACTIVE['ACTIVE'])