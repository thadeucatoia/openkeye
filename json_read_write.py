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


if __name__ == "__main__":
     write_json("tool_1", "low_rgb", 456)
     write_json("tool_1", "high_rgb", 123)