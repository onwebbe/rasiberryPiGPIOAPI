INTERFACE = {
  'GPIO': 0,
  'PWM': 1,
  'I2C': 2
}
PIN_MODE = {
  "IN": 0,
  "OUT": 1,
  "I2C": 2
}
PIN_FUCNTION = {
  'GND': 0,
  'GPIO': 1,
  '3V': 2,
  '5V': 3,
  'SDA': 4,
  'SDL': 5
}
STATUS = {
  'UNBIND': 0,
  'BIND': 1
}

def getDictKeyByName(dictObject, value):
  for (key, itemValue) in dictObject.items():
    if (value == itemValue):
      return key
  return None