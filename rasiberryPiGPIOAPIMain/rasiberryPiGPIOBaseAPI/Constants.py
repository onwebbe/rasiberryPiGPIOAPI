SCHEDULE_MODE = {
  'SECONDS': 1,
  'MINUTS': 2,
  'HOUR': 3,
  'DAY': 4
}
SCHEDULE_STATUS = {
  'RUNNING': 1,
  'STOPPED': 2
}
SCHEDULE_ACTIVE = {
  'ACTIVE': 1,
  'DEACTIVE': 2
}
def getDictKeyByName(dictObject, value):
  for (key, itemValue) in dictObject.items():
    if (value == itemValue):
      return key
  return None