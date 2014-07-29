import json

### Functions to read config.json ###

# retrieve list of ignored files
def getIgnoredFiles():
  json_data = open("config.json")
  configData = json.load(json_data)
  json_data.close()
  return configData["ignored_files"]
