import json
class MyEncoder(json.JSONEncoder):
  def default(self, obj):  # pylint: disable=E0202
    return json.JSONEncoder.default(self, obj)