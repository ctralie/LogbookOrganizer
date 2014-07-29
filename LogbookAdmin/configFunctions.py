import json

def getIgnoredFiles():
  json_data = open("config.json")
  configData = json.load(json_data)
  json_data.close()
  return configData["ignored_files"]
