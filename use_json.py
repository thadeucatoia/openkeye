import json
import os

def write_json(tool_number, par, value):
    archive = os.path.join(os.path.dirname(__file__), 'refs', 'tool_reference.json')
    with open(archive) as json_file:
        data = json.load(json_file)
        json_file.close()

    data[tool_number][par] = value
    

    json_file = open(archive, "w+")
    json_file.write(json.dumps(data, indent=2))
    json_file.close()

def read_json(tool_number, par):
    archive = os.path.join(os.path.dirname(__file__), 'refs', 'tool_reference.json')
    with open(archive) as json_file:
        data = json.load(json_file)
        json_file.close()
    return data[tool_number][par]






